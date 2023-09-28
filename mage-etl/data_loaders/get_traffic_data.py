import io
import pandas as pd
import requests
from pandas import DataFrame
from datetime import datetime

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def get_urls(year=2023):
    """URL constructor for api.viz.berlin.de traffic data.

    Args:
        year (int, optional): How far back in time will the URLs / data go. Defaults to 2023.

    Returns:
        urls_list: List of URLs pointing to gzip csv of traffic data in Berlin
    """
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    start_url = "https://mdhopendata.blob.core.windows.net/verkehrsdetektion/"
    urls_list = []

    for year in range(year, current_year + 1):
        # 2021 and 2023 have different url patterns
        if year == 2021:
            mid_url = f"{year}/Messquerschnitt/mq_hr_{year}_"
        elif year == 2023:
            mid_url = f"{year}/Messquerschnitte%20(fahrtrichtungsbezogen)/mq_hr_{year}_"
        else:
            mid_url = f"{year}/Messquerschnitt%20(fahrtrichtungsbezogen)/mq_hr_{year}_"
        base_url = start_url + mid_url

        # Loop through every month of the year
        for month in range(1, 13):
            # Break if current year, current month is reached
            if year == current_year and month == current_month:
                break
            # Complete the URL and append to list
            appendix = f"{month:02d}.csv.gz"
            url = base_url + appendix
            urls_list.append(url)
    return urls_list


@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    """
    Fetches single gzip csv files, reads into pd.DataFrame and concatenates them into
    one dataframe and returns it.
    """
    # Pass a year between 2015-2022 to date the data further back
    urls_list = get_urls(2019)

    for index, url in enumerate(urls_list):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = io.BytesIO(response.content)
            if index == 0:
                df = pd.read_csv(data, compression="gzip", delimiter=";")
            else:
                df_next = pd.read_csv(data, compression="gzip", delimiter=";")
                df = pd.concat([df, df_next])
        except requests.exceptions.HTTPError as errh:
            print(f"{url[-14:]} not found")
    return df


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, "The output is undefined"
