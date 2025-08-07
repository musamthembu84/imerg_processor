import os
from dotenv import load_dotenv
from imerg_processor import ImergProcessor


def main():
    load_dotenv()
    processor = ImergProcessor(
        start_date=os.getenv("START_DATE"),
        end_date=os.getenv("END_DATE"),
        base_url=os.getenv("BASE_URL"),
        auth=(os.getenv("GESDISC_USERNAME"), os.getenv("GESDISC_TOKEN")),
        country_name=os.getenv("COUNTRY_NAME"),
        repo_id=os.getenv("HF_REPO_ID"),
        hf_token=os.getenv("HF_TOKEN")
    )

    processor.run(
        lat_north=float(os.getenv("LAT_NORTH")),
        lat_south=float(os.getenv("LAT_SOUTH")),
        lon_east=float(os.getenv("LON_EAST")),
        lon_west=float(os.getenv("LON_WEST")),
    )


if __name__ == "__main__":
    main()
