import pandas as pd
import pytest


@pytest.fixture()
def prices():
    return "tests/test_files/test_prices.csv"


@pytest.fixture()
def invalid_prices():
    return "tests/test_files/test_prices_invalid.csv"


@pytest.fixture()
def currency():
    return "tests/test_files/test_currency.csv"


@pytest.fixture()
def portfolio_definition():
    portfolio_definition = {
        "TEST": {"weight": 1, "currency": "usd"},
    }
    return portfolio_definition


@pytest.fixture()
def clean_returns():
    df = pd.read_csv("tests/test_files/test_returns.csv")
    df.returns.dropna(inplace=True)
    return df.returns
