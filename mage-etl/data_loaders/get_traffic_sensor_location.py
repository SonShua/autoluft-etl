import io
import pandas as pd
import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loaderet
def load_data_from_api(*args, **kwargs):
    """Loads the location data of the traffic sensors in Berlin (VIZ Berlin)

    Returns:
        pandas.Dataframe: _description_
    """
    url = "https://mdhopendata.blob.core.windows.net/verkehrsdetektion/Stammdaten_Verkehrsdetektion_2022_07_20.xlsx"
    response = requests.get(url)

    return pd.read_excel(io.BytesIO(response.content))


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
