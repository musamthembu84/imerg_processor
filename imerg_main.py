import os
from dotenv import load_dotenv
from imerg_processor import ImergProcessor
#
# def main():
#     load_dotenv()
#
#     processor = ImergProcessor(
#         start_date=os.getenv("START_DATE"),
#         end_date=os.getenv("END_DATE"),
#         base_url=os.getenv("BASE_URL"),
#         auth=(os.getenv("GESDISC_USERNAME"), os.getenv("GESDISC_TOKEN")),
#         country_name=os.getenv("COUNTRY_NAME"),
#         repo_id=os.getenv("HF_REPO_ID"),  # e.g. musamthembu84/imerg
#         hf_token=os.getenv("HF_TOKEN")  # Hugging Face access token
#     )
#
#     processor.run(
#         lat_north=float(os.getenv("LAT_NORTH")),
#         lat_south=float(os.getenv("LAT_SOUTH")),
#         lon_east=float(os.getenv("LON_EAST")),
#         lon_west=float(os.getenv("LON_WEST")),
#     )
#
#
# if __name__ == "__main__":
#     main()


from imerg_processor import ImergProcessor

def main():
    processor = ImergProcessor(
        start_date="2022-01-01",
        end_date="2022-01-10",
        base_url="https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGDF.07",
        auth=("random", "random"),
        country_name="Kenya",
        repo_id="random",
        hf_token="removetokens"
    )

    processor.run(
        lat_north=5.0,
        lat_south=-5.0,
        lon_east=42.0,
        lon_west=33.0,
    )

if __name__ == "__main__":
    main()
