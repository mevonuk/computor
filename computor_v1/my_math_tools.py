# mathematical tools

def abs(x: int | float) -> int | float:
    """Returns absolute value of x"""
    if not isinstance(x, (int, float)):
        raise TypeError("for abs, x must be int/float")
    if x >= 0:
        return x
    else:
        return -x


def sqrt(x: int | float) -> int | float:
    """Returns sqrt of x"""
    if not isinstance(x, (int, float)):
        raise TypeError("for sqrt, x must be int/float")
    last_guess = x / 2.0
    epsilon = .00000000000001
    while True:
        guess = (last_guess + x / last_guess) / 2
        if abs(guess - last_guess) < epsilon:
            return guess
        last_guess = guess


def reduce(b: int | float, a: int | float, mode: int) -> str:
    """reduce integer faction b/a if possible,
    otherwise just divide,
    mode = 1 indicates number is complex
    returns string with reduced fraction"""
    if not isinstance(b, (int, float)):
        raise TypeError("for reduce, b must be int/float")
    if not isinstance(a, (int, float)):
        raise TypeError("for reduce, a must be int/float")
    if not isinstance(mode, int):
        raise TypeError("for reduce, mode must be int")
    if mode not in {0, 1}:
        raise Exception("Error: for reduce, mode must be 0 or 1")

    if isinstance(b, int) and isinstance(a, int):
        if a * b > 0:
            a = int(abs(a))
            b = int(abs(b))
        factor = 2
        while factor <= min(abs(a), abs(b)):
            while b % factor == 0 and a % factor == 0:
                b = int(b/factor)
                a = int(a/factor)
            factor += 1
        s = f"{b}/{a}"
        if mode == 1:
            s = f"{b}i/{a}"
        if abs(b) % abs(a) == 0:
            c = int(b/a)
            s = f"{c}"
            if mode == 1:
                s = f"{c}i"
        if abs(b) == abs(a):
            if b * a < 0:
                s = "-1"
            else:
                s = "1"
            if mode == 1:  # don't worry about negative i
                s = "i"
    else:
        c = b/a
        c = int(c) if c.is_integer() else c
        s = f"{c}"
        if mode == 1:
            s = f"{c}i"
    return s
