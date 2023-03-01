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
        valid = validation.validate_columns(df, columns)
        assert valid
    except validation.InvalidDataFrame:
        pytest.fail("Should not raise InvalidDataFrame")


def test_validate_columns_invalid(invalid_prices):
    """
    GIVEN an invalid dataframe of prices
    WHEN validation.validate_columns is called
    THEN it will raise an Exception
    """
    df = pd.read_csv(invalid_prices)
    columns = ["TIDM", "Date", "Open", "High", "Low", "Close", "Volume", "Adjustment"]
    with pytest.raises(validation.InvalidDataFrame):
        validation.validate_columns(df, columns)


def test_validate_datatypes_valid(prices):
    """
    GIVEN a valid dataframe of prices
    WHEN validation.validate_datatypes is called
    THEN it will return valid
    """
    df = pd.read_csv(prices)
    datatypes = {
        "TIDM": "string",
        "Date": "string",
        "Open": float,
        "High": float,
        "Low": float,
        "Close": float,
        "Volume": float,
        "Adjustment": float,
    }
    try:
        valid = validation.validate_datatypes(df, datatypes)
        assert valid
    except validation.InvalidDataFrame:
        pytest.fail("Should not raise InvalidDataFrame")


def test_validate_datatypes_invalid(invalid_prices):
    """
    GIVEN an invalid dataframe of prices
    WHEN validation.validate_datatypes is called
    THEN it will raise an Exception
    """
    df = pd.read_csv(invalid_prices)
    datatypes = {
        "TIDM": "string",
        "Date": "string",
        "Open": float,
        "High": float,
        "Low": float,
        "Close": float,
        "Volume": float,
    }
    with pytest.raises(validation.InvalidDataFrame):
        validation.validate_columns(df, datatypes)


@pytest.mark.parametrize(
    "definition,expected",
    [
        ({"EG": {"weight": 1, "currency": "gbp"}}, True),
        (
            {
                "EG": {"weight": 0.9, "currency": "gbp"},
                "EG2": {"weight": 1, "currency": "gbp"},
            },
            False,
        ),
        (
            {
                "EG": {"weight": 0.9, "currency": "eur"},
                "EG2": {"weight": 0.1, "currency": "gbp"},
            },
            False,
        ),
        (
            {"EG": {"weight": 1}},
            False,
        ),
        (
            {"EG": {"currency": "gbp"}},
            False,
        ),
    ],
)
def test_validate_portfolio_definition(definition, expected):
    """
    GIVEN an invalid portfolio definition
    WHEN validation.validat_portfolio_definition
    THEN it will raise and exception
    """
    if expected:
        try:
            valid = validation.validate_portfolio_definition(definition)
            assert valid
        except validation.InvalidPortfolioDefinition:
            pytest.fail("Should not raise InvalidPortfolioDefinition")
    else:
        with pytest.raises(validation.InvalidPortfolioDefinition):
            validation.validate_portfolio_definition(definition)
