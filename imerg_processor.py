import os
import requests
import tempfile
from datetime import datetime, timedelta

import xarray as xr
from huggingface_hub import HfApi


class ImergProcessor:
    def __init__(self, start_date, end_date, base_url, auth, country_name, repo_id, hf_token):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.base_url = base_url
        self.auth = auth
        self.country_name = country_name
        self.repo_id = repo_id
        self.api = HfApi(token=hf_token)

        # Fetch and cache existing file list ONCE
        file_list = self.api.list_repo_files(repo_id=self.repo_id, repo_type="dataset")
        self.existing_files = set(file_list)  # Use a set for fast membership checks
        print(f"Found {len(self.existing_files)} existing files in repo.")

        print("Auth username:", self.auth[0])
        print("Auth password:", (self.auth[1]))

    def run(self, lat_north, lat_south, lon_east, lon_west):
        for date in self._date_range():
            filename, url = self._build_url_and_filename(date)
            final_filename = filename.replace(".nc4", f"_{self.country_name}.nc4")
            remote_path = f"{self.country_name}/{final_filename}"

            if remote_path in self.existing_files:
                print(f"File already exists on remote storage: {remote_path}, skipping.")
                continue

            try:
                print(f"Downloading and processing {filename}")
                file_bytes = self._download_file_to_memory(url)
                self._process_and_upload_file(file_bytes, final_filename, remote_path, lat_north, lat_south, lon_east, lon_west)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    def _date_range(self):
        current = self.start_date
        while current <= self.end_date:
            yield current
            current += timedelta(days=1)

    def _build_url_and_filename(self, date):
        date_str = date.strftime("%Y%m%d")
        year = date.strftime("%Y")
        month = date.strftime("%m")
        filename = f"3B-DAY.MS.MRG.3IMERG.{date_str}-S000000-E235959.V07B.nc4"
        url = f"{self.base_url}/{year}/{month}/{filename}"
        return filename, url

    def _download_file_to_memory(self, url):
        response = requests.get(url, auth=self.auth, stream=True, timeout=60)
        if response.status_code != 200:
            raise Exception(f"Download failed with status code {response.status_code}")
        print(" Downloaded file to memory")
        return response.content

    def _process_and_upload_file(self, file_bytes, final_filename, remote_path, lat_north, lat_south, lon_east, lon_west):
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_nc4_path = os.path.join(temp_dir, "raw_download.nc4")
            processed_nc4_path = os.path.join(temp_dir, final_filename)

            # Write raw bytes to a temp file for xarray to open
            with open(raw_nc4_path, "wb") as f:
                f.write(file_bytes)

            ds = xr.open_dataset(raw_nc4_path)

            lat_slice = slice(lat_south, lat_north) if ds.lat[0] < ds.lat[-1] else slice(lat_north, lat_south)
            ds_region = ds.sel(lat=lat_slice, lon=slice(lon_west, lon_east))

            precip_var = 'precipitation' if 'precipitation' in ds_region.data_vars else list(ds_region.data_vars)[0]

            if ds_region[precip_var].count().item() == 0:
                print("No precipitation data found. Skipping upload.")
                ds.close()
                return

            ds_region.to_netcdf(processed_nc4_path)
            print(f"Saved processed file: {processed_nc4_path}")
            ds.close()

            # Upload with country subfolder path_in_repo
            self.api.upload_file(
                path_or_fileobj=processed_nc4_path,
                path_in_repo=remote_path,
                repo_id=self.repo_id,
                repo_type="dataset"
            )
            print(f"Uploaded to remote storage: {remote_path}")

            print("Temporary files cleaned up.")

