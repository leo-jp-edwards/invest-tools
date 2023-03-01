import typing

import numpy as np
import pandas as pd

# import statsmodels.formula.api as smf
from scipy import stats


def calculate_mean_daily_returns(clean_returns: pd.Series) -> float:
    return np.mean(clean_returns)


def calculate_mean_annual_return(clean_returns: pd.Series) -> float:
    mean_returns = calculate_mean_daily_returns(clean_returns)
    return ((1 + mean_returns) ** 252) - 1


def calculate_std_daily(clean_returns: pd.Series) -> float:
    return np.std(clean_returns)


def calculate_variance_daily(clean_returns: pd.Series) -> float:
    return calculate_std_daily(clean_returns) ** 2


def calculate_skewness(clean_returns: pd.Series) -> float:
    return stats.skew(clean_returns)


def calculate_kurtosis(clean_returns: pd.Series) -> float:
    return stats.kurtosis(clean_returns)


def calculate_shapiro(clean_returns: pd.Series) -> typing.Tuple[float, float]:
    """
    Calculate shapiro and p-value
    """
    shapiro = stats.shapiro(clean_returns)
    return shapiro[0], shapiro[1]


def calculate_percentage_returns(clean_returns: pd.Series) -> float:
    percent = clean_returns * 100
    return percent.dropna()
