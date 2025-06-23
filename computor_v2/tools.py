# contains get_value, get_value2

from variable import Variable


def get_value(value, history):
    """returns either the value from hisotry or None"""
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
