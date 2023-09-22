if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(fact_table, *args, **kwargs):
    """Takes fact_table, write datetime_id to new dataframe
    and delete all duplication. Extract weekday, hour, day, month and year each
    into new columns.

    Args:
        fact_table (pandas.DataFrame): Traffic data containing datetime_id column

    Returns:
        datetime_dim: dimensional dataframe for datetime information
    """
    # Specify your transformation logic here

    # Datetime dimension table from fact table
    datetime_dim = fact_table[["datetime_id"]].reset_index(drop=True)
    # Delete all the duplication
    datetime_dim = datetime_dim.drop_duplicates().reset_index(drop=True)
    datetime_dim["weekday"] = datetime_dim["datetime_id"].dt.weekday
    datetime_dim["hour"] = datetime_dim["datetime_id"].dt.hour
    datetime_dim["day"] = datetime_dim["datetime_id"].dt.day
    datetime_dim["month"] = datetime_dim["datetime_id"].dt.month
    datetime_dim["year"] = datetime_dim["datetime_id"].dt.year

    return datetime_dim


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
