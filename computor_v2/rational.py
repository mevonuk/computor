import sys
from complex import Complex
from matrix import Matrix
from variable import Variable

class Rational(Complex):
	def __init__(self, value):
		if isinstance(value, int) or isinstance(value, float):
			Complex.__init__(self, value, 0)
		else:
			print("Value is not rational")
			sys.exit()

	def __str__(self):
		return str(self.real)

	def __add__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.real + o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.real + o.real)
			return new_rational
		elif isinstance(o, Complex):
			new_complex = Complex(self.real + o.real, o.imag)
			return new_complex
		else:
			print("Bad input in r add function")
			return None

	def __radd__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.real + o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.real + o.real)
			return new_rational
		elif isinstance(o, Complex):
			new_complex = Complex(self.real + o.real, o.imag)
			return new_complex
		else:
			print("Bad input in r radd function")
			return None

	def __sub__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.real - o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.real - o.real)
			return new_rational
		elif isinstance(o, Complex):
			new_complex = Complex(self.real - o.real, -o.imag)
			return new_complex
		else:
			print("Bad input in r sub function")
			return None

	def __rsub__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(o - self.real)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(-self.real + o.real)
			return new_rational
		elif isinstance(o, Complex):
			new_complex = Complex(-self.real + o.real, o.imag)
			return new_complex
		else:
			print("Bad input in r rsub function")
			return None

	def __mul__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.real * o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.real * o.real)
			return new_rational
		elif isinstance(o, Complex):
			convert = Complex(self.real, 0)
			new_complex = convert * o
			return new_complex
		elif isinstance(o, Matrix):
			return o * self
		elif isinstance(o, Variable):
			return o.value * self
		else:
			print("Bad input in r mul function")
			return None

	def __rmul__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.real * o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.real * o.real)
			return new_rational
		elif isinstance(o, Complex):
			convert = Complex(self.real, 0)
			new_complex = convert * o
			return new_complex
		elif isinstance(o, Variable):
			return o.value * self
		else:
			print(o, type(o))
			print("Bad input in r rmul function")
			return None

	def __truediv__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.real / o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.real / o.real)
			return new_rational
		elif isinstance(o, Complex):
			convert = Complex(self.real, 0)
			new_complex = convert / o
			return new_complex
		else:
			print("Bad input in r truediv function")
			return None

	def __rtruediv__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(o / self.real)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(o.real / self.real)
			return new_rational
		elif isinstance(o, Complex):
			convert = Complex(self.real, 0)
			new_complex = o / convert
			return new_complex
		else:
			print("Bad input in r rtruediv function")
			return None

	def __mod__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(self.real % o)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(self.real % o.real)
			return new_rational
		else:
			print("Bad input in r mod function")
			return None

	def __rmod__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_rational = Rational(o % self.real)
			return new_rational
		elif isinstance(o, Rational):
			new_rational = Rational(o.real % self.real)
			return new_rational
		else:
			print("Bad input in r rmod function")
			return None

	def __pow__(self, n):
		if isinstance(n, int) or isinstance(n, float):
			new_rational = Rational(self.real ** n)
			return new_rational
		elif isinstance(n, Rational):
			new_rational = Rational(self.real ** n.real)
			return new_rational
		elif isinstance(n, Complex) and n.imag == 0:
			new_rational = Rational(self.real ** n.real)
			return new_rational
		else:
			print("Bad input in r pow function")
			return None

	def __rpow__(self, n):
		if isinstance(n, int) or isinstance(n, float):
			new_rational = Rational(n ** self.real)
			return new_rational
		elif isinstance(n, Rational):
			new_rational = Rational(n.real ** self.real)
			return new_rational
		elif isinstance(n, Complex) and n.imag == 0:
			new_rational = Rational(self.real ** n.real)
			return new_rational
		else:
			print("Bad input in r rpow function")
			return None

	def __neg__(self):
		new_rational = Rational(- self.real)
		return new_rational