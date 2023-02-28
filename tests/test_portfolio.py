from invest_tools.portfolio import Currency, Portfolio


def test_portfolio_ping():
    """
    GIVEN
    WHEN Portfolio.ping is called
    THEN ping is returned
    """
    cur = Currency.GBP
    ping = Portfolio(cur).ping()
    assert ping == "pong"


def test_portfolio_calculate_returns(prices, currency):
    """
    GIVEN a csv of prices and currency
    WHEN portfolio.calculate_returns is called
    THEN a DataFrame is returned
    """
    cur = Currency.GBP
    port = Portfolio(cur)
    prices_df = port.get_prices(prices)
    test_code = "TEST"
    port.get_usd_converter(currency)
    returns = port.calculate_returns(
        prices_df, test_code, convert=True, cur=port.gbpusd
    )
    assert len(returns) > 0


def test_portfolio_get_usd_converter(currency):
    """
    GIVEN a csv of currency
    WHEN portfolio.get_usd_converter is called
    THEN a class attribute is defined
    """
    cur = Currency.GBP
    port = Portfolio(cur)
    port.get_usd_converter(currency)
    assert len(port.gbpusd) > 0


def test_portfolio_get_prices(prices):
    """
    GIVEN a csv of prices
    WHEN portfolio.get_prices is called
    THEN a class attribute is defined
    """
    cur = Currency.GBP
    port = Portfolio(cur)
    port.get_prices(prices)
    assert len(port.prices) > 0


def test_portfolio_build(currency, prices):
    """
    GIVEN a portfolio definition
    WHEN portfolio.build is called
    THEN a backtest attribute is created and calculated
    """
    portfolio_definition = {
        "TEST": {"weight": 1, "currency": "usd"},
    }
    cur = Currency.GBP
    port = Portfolio(portfolio_definition, cur)
    port.get_usd_converter(currency)
    port.get_prices(prices)
    port.build()
    assert len(port.backtest) > 0
