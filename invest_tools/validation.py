import typing

import pandas as pd

from invest_tools.currency import Currency


class InvalidDataFrame(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidPortfolioDefinition(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_columns(df: pd.DataFrame, columns: typing.List[str]) -> bool:
    if list(df.columns) != columns:
        diff = []
        for col in df.columns:
            if col not in columns:
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
            raise InvalidPortfolioDefinition(f"{opts['currency']} not permitted")
        weights.append(opts["weight"])
    weights = sum(weights)
    if weights != 1:
        raise InvalidPortfolioDefinition(f"total weights of {weights} should be 1")
    return True
