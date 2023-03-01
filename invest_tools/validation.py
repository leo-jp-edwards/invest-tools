import math
import typing

import numpy as np
import pandas as pd

from invest_tools.currency import Currency, InvalidCurrencyException


class InvalidDataFrame(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidPortfolioDefinition(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_columns(df: pd.DataFrame, columns: typing.List[str]) -> bool:
    if set(df.columns) != set(columns):
        diff = []
        for col in set(df.columns):
            if col not in set(columns):
                diff.append(col)
        raise InvalidDataFrame(f"Invalid DataFrame due to column error: {diff}")
    else:
        return True


def validate_datatypes(df: pd.DataFrame, column_types: typing.Dict[str, str]) -> bool:
    try:
        df = df.astype(column_types)
        return True
    except ValueError as e:
        raise InvalidDataFrame(f"Invalid DataFrame due to datatype error: {e}")


def validate_portfolio_definition(
    definition: typing.Dict[str, typing.Dict[str, str]]
) -> bool:
    weights = []
    currencies = set(currency.value for currency in Currency)
    for code, opts in definition.items():
        if "weight" not in opts.keys():
            raise InvalidPortfolioDefinition(f"weight definition missing from {code}")
        if "currency" not in opts.keys():
            raise InvalidPortfolioDefinition(f"currency definition missing from {code}")
        if opts["currency"] not in currencies:
            raise InvalidCurrencyException(f"{opts['currency']} not permitted")
        weights.append(opts["weight"])
    total_weight = np.sum(weights)
    # floating point precsion + rounding means that sometimes this is not 1 exactly
    if not math.isclose(total_weight, 1):
        raise InvalidPortfolioDefinition(f"total weights of {total_weight} should be 1")
    return True
