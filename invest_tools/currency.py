from enum import Enum


class Currency(Enum):
    USD = "usd"
    GBP = "gbp"


class InvalidCurrencyException(Exception):
    "Raised when the currency input is invalid"
    pass
