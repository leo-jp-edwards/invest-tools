import typing

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats


def calculate_mean_daily_returns(clean_returns: pd.Series) -> np.ndarray:
    return np.mean(clean_returns)


def calculate_mean_annual_return(clean_returns: pd.Series) -> float:
    mean_returns = calculate_mean_daily_returns(clean_returns)
    return ((1 + mean_returns) ** 252) - 1


def calculate_std_daily(clean_returns: pd.Series) -> np.ndarray:
    return np.std(clean_returns)


def calculate_variance_daily(clean_returns: pd.Series) -> float:
    return calculate_std_daily(clean_returns) ** 2


def calculate_skewness(clean_returns: pd.Series) -> np.ndarray:
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


def calculate_beta_cov(backtest_data: pd.DataFrame) -> float:
    """
    Calculate beta using covariance

    $$ \beta P = \frac{Cov(RP, RB)}{Var(RB)} $$
    """
    covariance_matrix = backtest_data.cov()
    covariance_coefficient = covariance_matrix.iloc[0, 1]
    benchmark_variance = backtest_data["benchmark_returns"].var()
    portfolio_beta = covariance_coefficient / benchmark_variance
    return portfolio_beta


def calculate_beta_capm(backtest_data: pd.DataFrame) -> float:
    capm_model = smf.ols(
        formula="portfolio_returns ~ benchmark_returns", data=backtest_data
    )
    capm_fit = capm_model.fit()
    regression_beta = capm_fit.params["benchmark_returns"]
    return regression_beta


def calculate_max_drawdown(cumulative_returns: pd.Series) -> np.ndarray:
    """
    Calculate historical drawdown
    """
    running_max = np.maximum.accumulate(cumulative_returns)
    running_max[running_max < 1] = 1
    drawdown = cumulative_returns / running_max - 1
    return np.max(np.array(drawdown))
