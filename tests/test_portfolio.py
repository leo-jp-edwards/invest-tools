from invest_tools.currency import Currency
from invest_tools.portfolio import Portfolio


def test_portfolio_ping(portfolio_definition):
    """
    GIVEN
    WHEN Portfolio.ping is called
    THEN ping is returned
    """
    cur = Currency.GBP
    ping = Portfolio(portfolio_definition, cur).ping()
    assert ping == "pong"


def test_portfolio_calculate_returns(portfolio_definition, prices, currency):
    """
    GIVEN a csv of prices and currency
    WHEN portfolio.calculate_returns is called
    THEN a DataFrame is returned
    """
    cur = Currency.GBP
    port = Portfolio(portfolio_definition, cur)
    prices_df = port.get_prices(prices)
    test_code = "TEST"
    port.get_usd_converter(currency)
    returns = port.calculate_returns(
        prices_df, test_code, convert=True, cur=port.gbpusd
    )
    assert len(returns) > 0


def test_portfolio_get_usd_converter(portfolio_definition, currency):
    """
    GIVEN a csv of currency
    WHEN portfolio.get_usd_converter is called
    THEN a class attribute is defined
    """
    cur = Currency.GBP
    port = Portfolio(portfolio_definition, cur)
    port.get_usd_converter(currency)
    assert len(port.gbpusd) > 0


def test_portfolio_get_prices(portfolio_definition, prices):
    """
    GIVEN a csv of prices
    WHEN portfolio.get_prices is called
    THEN a class attribute is defined
    """
    cur = Currency.GBP
    port = Portfolio(portfolio_definition, cur)
    port.get_prices(prices)
    assert len(port.prices) > 0


def test_portfolio_build(portfolio_definition, currency, prices):
    """
    GIVEN a portfolio definition
    WHEN portfolio.build is called
    THEN a backtest attribute is created and calculated
    """
    cur = Currency.GBP
    port = Portfolio(portfolio_definition, cur)
    port.get_usd_converter(currency)
    port.get_prices(prices)
    port.build()
    assert len(port.backtest) > 0


def test_portfolio_analyse(portfolio_definition, currency, prices):
    """
    GIVEN a portfolio that has already been built
    WHEN portfolio.analyse is called
    THEN an analysis attribute is calculated
    """
    cur = Currency.GBP
    port = Portfolio(portfolio_definition, cur)
    port.get_usd_converter(currency)
    port.get_prices(prices)
    port.build()
    port.analyse()

    assert "daily_returns" in port.analysis
    assert "annual_returns" in port.analysis
    assert "daily_std" in port.analysis
    assert "daily_var" in port.analysis
    assert "skew" in port.analysis
    assert "kurtosis" in port.analysis

    assert len(port.percentage_returns) > 0


def test_benchmark_analysis(portfolio_definition, currency, prices, benchmark):
    """
    GIVEN a portfolio that has already been built
    WHEN portfolio.benchmark is called
    THEN a benchmark attribute is calculated
    """
    cur = Currency.GBP
    port = Portfolio(portfolio_definition, cur)
    port.get_usd_converter(currency)
    port.get_prices(prices)
    port.build()
    port.get_benchmark(benchmark)

    assert "benchmark_returns" in port.backtest

    port.benchmark_analysis()

    assert len(port.benchmark) > 0
