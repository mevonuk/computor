# contains get_value, get_value2

from variable import Variable
from rational import Rational


def get_value(value, history):
    """returns either the value from history or None"""
    if value in history:
        result = history[value]
        if isinstance(result, str):
            result = get_value(result, history)
        if isinstance(result, Variable):
            result = result.value
        return result
    return None


def get_value2(value, history):
    """Returns either the value from history or itself"""
    if value in history:
        result = history[value]
        if isinstance(result, str):
            result = get_value2(result, history)
        if isinstance(result, Variable):
            result = result.value
        return result
    return value


def power_node(x, n):
    """Returns power"""
    if n == Rational(1):
        return x
    else:
        m = n - Rational(1)
        return x * power_node(x, m)
