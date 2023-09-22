import pandas as pd

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """Takes raw traffic data count from api.viz.berlin.de, creates column names according
    to data model and create datetime_id

    Args:
        data (pandas.DataFrame):
    Returns:
        fact_table (pandas.DataFrame): Cleaned raw data according to data model
    """
    # Name the columns as specified in data model create datetime_id from tag + hour
    fact_table = data.rename(
        columns={"mq_name": "mq_name_id", "tag": "date", "stunde": "hour"}
    )
    # Create datetime_id from date+hour
    fact_table["datetime_id"] = pd.to_datetime(
        fact_table["date"] + " " + fact_table["hour"].apply(str), format="%d.%m.%Y %H"
    )
    # Drop date and hour columns
    fact_table.drop(["date", "hour"], axis=1, inplace=True)

    # Drop possible duplication and reset the index
    fact_table = fact_table.drop_duplicates().reset_index(drop=True)

    # Remove trailing n from mq_name_id
    fact_table['mq_name_id'] = fact_table['mq_name_id'].map(lambda x: x.rstrip('n'))


    # Create a new index column
    fact_table["mess_id"] = fact_table.index

    return fact_table


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
