import pandas as pd
import pytest

from invest_tools import validation


def test_validate_columns_valid(prices):
    """
    GIVEN a valid dataframe of prices
    WHEN validation.validate_columns is called
    THEN it will return valid
    """
    df = pd.read_csv(prices)
    columns = ["TIDM", "Date", "Open", "High", "Low", "Close", "Volume", "Adjustment"]
    try:
        validation.validate_columns(df, columns)
    except validation.InvalidDataFrame:
        pytest.fail("Should not raise InvalidDataFrame")


def test_validate_columns_invalid(prices):
    """
    GIVEN an invalid dataframe of prices
    WHEN validation.validate_columns is called
    THEN it will raise and Exception
    """
    df = pd.read_csv(prices)
    columns = ["TIDM", "Date", "Open", "High", "Low", "Close", "Volume"]
    with pytest.raises(validation.InvalidDataFrame):
        validation.validate_columns(df, columns)
