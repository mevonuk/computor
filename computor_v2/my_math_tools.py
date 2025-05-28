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

# reduce integer faction if possible
def reduce(b, a, type):
	if type not in {0, 1}:
		print("Error: bad usage of reduce()")
		exit()

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
		if type == 1:
			s = f"{b}i/{a}"
		if abs(b) % abs(a) == 0:
			c = int(b/a)
			s = f"{c}"
			if type == 1:
				s = f"{c}i"
		if abs(b) == abs(a):
			if b * a < 0:
				s = f"-1"
			else:
				s = f"1"
			if type == 1: # don't worry about negative i
				s = f"i"
	else:
		c = b/a
		c = int(c) if c.is_integer() else c
		s = f"{c}"
		if type == 1:
			s = f"{c}i"
	return s

def quadratic(a, b, c):
		print("Solving quadratic equation...")
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