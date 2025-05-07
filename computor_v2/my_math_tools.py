def abs(x):
    if x >= 0:
        return x
    else:
        return -x

def sqrt(x):
    last_guess = x / 2.0
    epsilon = .00000000000001
    while True:
        guess = (last_guess + x / last_guess) / 2
        if abs(guess - last_guess) < epsilon:
            return guess
        last_guess = guess

def factoral(x):
    result = 1
    for i in range(1, x + 1):
        result *= i
    return result

def sin(x):
    # in radians
    result = x
    sign = -1
    for i in range(3, 31, 2):
        result += sign * x**i / factoral(i)
        sign *= -1
    return result

def cos(x):
    # in radians
    result = 1
    sign = -1
    for i in range(2, 32, 2):
        result += sign * x**i / factoral(i)
        sign *= -1
    return result

def atan(x):
    return x / (1 + 9 * x**2 / 32)