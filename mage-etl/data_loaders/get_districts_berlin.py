import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Loads geojson data for Berlins districts borders (polygons, geometry)
    and saves it to data folder
    """
    url = 'https://tsb-opendata.s3.eu-central-1.amazonaws.com/bezirksgrenzen/bezirksgrenzen.geojson'
    response = requests.get(url)
    data = response.content
    with open('data/bezirksgrenzen.geojson', 'wb') as f:
        f.write(data)



