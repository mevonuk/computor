# mathematical tools: abs, sqrt, factorial, sin, cos, atan, reduce, quadratic

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


def factoral(x: int) -> int:
    """Computes factorial of x"""
    if not isinstance(x, int):
        raise TypeError("for factorial, x must be int")
    result = 1
    for i in range(1, x + 1):
        result *= i
    return result


def sin(x: int | float) -> float:
    """Calculates the sine of x in radians"""
    if not isinstance(x, (int, float)):
        raise TypeError("for sin, x must be int/float")
    result = x
    sign = -1
    for i in range(3, 31, 2):
        result += sign * x**i / factoral(i)
        sign *= -1
    return result


def cos(x: int | float) -> float:
    """Calculates the cosine of x in radians"""
    if not isinstance(x, (int, float)):
        raise TypeError("for cos, x must be int/float")
    result = 1
    sign = -1
    for i in range(2, 32, 2):
        result += sign * x**i / factoral(i)
        sign *= -1
    return result


def atan(x: int | float) -> float:
    """Calculates the atan of x in radians"""
    if not isinstance(x, (int, float)):
        raise TypeError("for atan, x must be int/float")
    return x / (1 + 9 * x**2 / 32)


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


def quadratic(a: float | int, b: float | int, c: float | int):
    """Solves a quadratic equation with coefficients a, b, c"""
    if not isinstance(a, (float, int)):
        raise TypeError("ABORT: for quadratic, a must be float/int")
    if not isinstance(b, (float, int)):
        raise TypeError("ABORT: for quadratic, b must be float/int")
    if not isinstance(c, (float, int)):
        raise TypeError("ABORT: for quadratic, c must be float/int")
    if a != 0:
        # print("Solving quadratic equation...")
        discriminant = b * b - 4 * a * c
        if discriminant > 0:
            print("\nDiscriminant is positive: two real solutions:")
            top = -b + sqrt(discriminant)
            top = int(top) if top.is_integer() else top
            print(reduce(top, 2 * a, 0))
            top = -b - sqrt(discriminant)
            top = int(top) if top.is_integer() else top
            print(reduce(top, 2 * a, 0))
        elif discriminant == 0:
            print("\nDiscriminant is zero: one real solution:")
            print(f"{reduce(-b, 2 * a, 0)}")
        else:
            print("\nDiscriminant is negative: two complex solutions:")
            reduced_realterm = reduce(-b, 2 * a, 0)
            sqrtd = sqrt(abs(discriminant))
            sd = int(sqrtd) if sqrtd.is_integer() else sqrtd
            reduced_imagterm = reduce(sd, 2 * a, 1)
            if reduced_imagterm and reduced_imagterm[0] == '-':
                reduced_imagterm = reduced_imagterm[1:]
            print(f"{reduced_realterm} + {reduced_imagterm}")
            print(f"{reduced_realterm} - {reduced_imagterm}")
    elif a == 0 and b != 0 and c != 0:
        print("Solving linear equation...")
        print("\nSolution:", reduce(-b, c, 0))
    elif a == 0 and b == 0 and c != 0:
        print("No solution for equation.")
    else:
        print("Solution given.")
