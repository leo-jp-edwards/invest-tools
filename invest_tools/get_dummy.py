import random

from invest_tools.dummy import test

def get_dummy() -> dict:
    """
    GET dummy

    Get randomly selected dummy from database of dummies

    :return: selected dummy
    :rtype: dict
    """
    return test[random.randint(0, len(test) - 1)]