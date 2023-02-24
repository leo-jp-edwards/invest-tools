from invest_tools.portfolio import Portfolio


def test_portfolio_ping():
    """
    GIVEN
    WHEN Portfolio.ping is called
    THEN ping is returned
    """
    ping = Portfolio().ping()
    assert ping == "ping"
