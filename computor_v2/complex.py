import sys

class Complex:
	def __init__(self, real_value, imag_value):
		if isinstance(real_value, int) or isinstance(real_value, float):
			self.real = real_value
		else:
			print("Value is not rational")
			sys.exit()
		if isinstance(imag_value, int) or isinstance(imag_value, float):
			self.imag = imag_value
		else:
			print("Value is not rational")
			sys.exit()

	def __str__(self):
		return str(self.real) + " + " + str(self.imag) + "i"

	def __add__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_complex = Complex(self.real + o, self.imag)
			return new_complex
		elif isinstance(o, Rational):
			new_complex = Rational(self.value + o.value)
			return new_complex
		else:
			print("Bad input in add function")
			return None

	def __radd__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_complex = Rational(self.value + o)
			return new_complex
		elif isinstance(o, Rational):
			new_rational = Rational(self.value + o.value)
			return new_rational
		else:
			print("Bad input in radd function")
			return None

	def __sub__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.value - o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.value - o.value)
			return new_rational
		else:
			print("Bad input in sub function")
			return None

	def __rsub__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(o - self.value)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(-self.value + o.value)
			return new_rational
		else:
			print("Bad input in rsub function")
			return None

	def __mul__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.value * o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.value * o.value)
			return new_rational
		else:
			print("Bad input in mul function")
			return None

	def __rmul__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.value * o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.value * o.value)
			return new_rational
		else:
			print("Bad input in rmul function")
			return None

	def __truediv__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.value / o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.value / o.value)
			return new_rational
		else:
			print("Bad input in truediv function")
			return None

	def __rtruediv__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(o / self.value)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(o.value / self.value)
			return new_rational
		else:
			print("Bad input in rtruediv function")
			return None

	def __mod__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.value % o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.value % o.value)
			return new_rational
		else:
			print("Bad input in mod function")
			return None

	def __rmod__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(o % self.value)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(o.value % self.value)
			return new_rational
		else:
			print("Bad input in rmod function")
			return None

	def __pow__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.value ** o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.value ** o.value)
			return new_rational
		else:
			print("Bad input in pow function")
			return None

	def __rpow__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(o ** self.value)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(o.value ** self.value)
			return new_rational
		else:
			print("Bad input in rpow function")
			return None