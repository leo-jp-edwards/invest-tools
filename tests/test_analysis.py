import pandas as pd
import pytest
from pandas import testing as tm

from invest_tools import analysis


def test_mean_daily_returns(clean_returns):
    """
    GIVEN a pandas series of returns
    WHEN calculate_mean_daily_returns is called
    THEN it returns the answer
    """
    mean = analysis.calculate_mean_daily_returns(clean_returns)
    assert mean == 0.003


def test_mean_annual_return(clean_returns):
    """
    GIVEN a pandas series of returns
    WHEN calculate_mean_annual_returns is called
    THEN it returns the answer

    Note test is approximate due to floating point precision
    """
    mean = analysis.calculate_mean_annual_return(clean_returns)
    assert mean == pytest.approx(1.12, 0.01)


def test_std_daily(clean_returns):
    """
    GIVEN a pandas series of returns
    WHEN calculate_std_daily is called
    THEN it returns the answer
    """
    std = analysis.calculate_std_daily(clean_returns)
    assert std == pytest.approx(0.00141, 0.01)


def test_variance_daily(clean_returns):
    """
    GIVEN a pandas series of returns
    WHEN calculate_variance_daily is called
    THEN it returns the answer
    """
    var = analysis.calculate_variance_daily(clean_returns)
    assert var == pytest.approx(2e-06, 0.01)


def test_skewness(clean_returns):
    """
    GIVEN a pandas series of returns
    WHEN calculate_skewness is called
    THEN it returns the answer
    """
    skew = analysis.calculate_skewness(clean_returns)
    assert skew == 0


def test_kurtosis(clean_returns):
    """
    GIVEN a pandas series of returns
    WHEN calculate_kurtosis is called
    THEN it returns the answer
    """
    kurt = analysis.calculate_kurtosis(clean_returns)
    assert kurt == pytest.approx(-1.3, 0.01)


def test_shapiro(clean_returns):
    """
    GIVEN a pandas series of returns
    WHEN calculate_shapiro is called
    THEN it returns the answers
    """
    shap, p_value = analysis.calculate_shapiro(clean_returns)
    assert shap == pytest.approx(0.987, 0.01)
    assert p_value == pytest.approx(0.967, 0.01)


def test_percentage_returns(clean_returns):
    """
    GIVEN a pandas series of returns
    WHEN calculate_percentage_returns is called
    THEN it returns the answer
    """
    pct = analysis.calculate_percentage_returns(clean_returns)
    true_pct = pd.Series([0.1, 0.2, 0.3, 0.4, 0.5], name="returns", dtype=float)
    tm.assert_series_equal(pct, true_pct)
