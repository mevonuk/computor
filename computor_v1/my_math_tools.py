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