if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: "Stammdaten_Verkehrsdetektion_2022_07_20.xlsx" loaded from api.viz-berlin.de

    Returns:
        location_dim (pandas.DataFrame):Dimensional df for traffic data. Join on mq_name_id with traffic data
    """
    data = data.rename(
        columns={
            "DET_ID15": "det_id",
            "MQ_KURZNAME": "mq_name_id",
            "LÄNGE (WGS84)": "lng",
            "BREITE (WGS84)": "lat",
            "POSITION": "desc",
        }
    )
    location_dim = data[["det_id", "mq_name_id", "lat", "lng", "desc"]]

    return location_dim


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
