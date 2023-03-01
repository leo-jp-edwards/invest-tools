from enum import Enum


class Currency(Enum):
    USD = "usd"
    GBP = "gbp"


class InvalidCurrencyException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
