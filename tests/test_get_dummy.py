from invest_tools import get_dummy
from invest_tools.dummy import test

def test_get_dummy():
    """
    GIVEN
    WHEN get_dummy is called
    THEN random dummy from test is returned
    """
    dummy = get_dummy()
    assert dummy in test