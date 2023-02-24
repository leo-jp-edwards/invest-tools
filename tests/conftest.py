import pytest

@pytest.fixture()
def prices():
    return "tests/test_files/test_prices.csv"

@pytest.fixture()
def currency():
    return "tests/test_files/test_currency.csv"