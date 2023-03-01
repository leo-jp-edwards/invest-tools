import typing

import pandas as pd


class InvalidDataFrame(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidPortfolioDefinition(Exception):
    def __init__(self, message):
        super().__init__(message)


def validate_columns(df: pd.DataFrame, columns: typing.List[str]) -> None:
    if list(df.columns) != columns:
        diff = []
        for col in df.columns:
            if col not in columns:
                diff.append(col)
        raise InvalidDataFrame(f"Invalid DataFrame due to column error: {diff}")
    else:
        pass


def validate_datatypes(df: pd.DataFrame, column_types: typing.Dict[str, str]) -> None:
    try:
        df = df.astype(column_types)
    except ValueError as e:
        raise InvalidDataFrame(f"Invalid DataFrame due to datatype error: {e}")


def validate_portfolio_definition(definition: typing.Dict[str, typing.Dict[str, str]]):
    for code, opts in definition.items():
        if "weight" not in opts.keys():
            raise InvalidPortfolioDefinition(f"weight definition missing from {code}")
        if "currency" not in opts.keys():
            raise InvalidPortfolioDefinition(f"currency definition missing from {code}")
    pass
