import sys
from my_math_tools import abs

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
		if self.imag == 0:
			return str(self.real)
		elif self.imag > 0:
			sign = ' + '
		else:
			sign = ' - '
		if self.real != 0:
			if abs(self.imag) == 1:
				return str(self.real) + sign + "i"
			else:
				return str(self.real) + sign + str(abs(self.imag)) + "i"
		else:
			if self.imag == 1:
				return "i"
			elif self.imag == -1:
				return "-i"
			else:
				return str(self.imag) + "i"

	def __add__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_complex = Complex(self.real + o, self.imag)
			return new_complex
		elif isinstance(o, Complex):
			new_complex = Complex(self.real + o.real, self.imag + o.imag)
			return new_complex
		else:
			print("Bad input in add function")
			return None

	def __radd__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_complex = Complex(self.real + o, self.imag)
			return new_complex
		elif isinstance(o, Complex):
			new_complex = Complex(self.real + o.real, self.imag + o.imag)
			return new_complex
		else:
			print("Bad input in radd function")
			return None

	def __sub__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_complex = Complex(self.real - o, self.imag)
			return new_complex
		elif isinstance(o, Complex):
			new_complex = Complex(self.real - o.real, self.imag - o.imag)
			return new_complex
		else:
			print("Bad input in sub function")
			return None

	def __rsub__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_complex = Complex(o - self.real, -self.imag)
			return new_complex
		elif isinstance(o, Complex):
			new_complex = Complex(-self.real + o.real, o.imag - self.imag)
			return new_complex
		else:
			print("Bad input in rsub function")
			return None

	def __mul__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_complex = Complex(self.real * o, self.imag * o)
			return new_complex
		elif isinstance(o, Complex):
			a = self.real
			b = self.imag
			c = o.real
			d = o.imag
			new_complex = Complex(a * c - b * d, a * d + b * c)
			return new_complex
		else:
			print("Bad input in mul function")
			return None

	def __rmul__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_complex = Complex(self.real * o, self.imag * o)
			return new_complex
		elif isinstance(o, Complex):
			a = o.real
			b = o.imag
			c = self.real
			d = self.imag
			new_complex = Complex(a * c - b * d, a * d + b * c)
			return new_complex
		else:
			print("Bad input in rmul function")
			return None

	def __truediv__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			new_complex = Complex(self.real / o, self.imag / o)
			return new_complex
		elif isinstance(o, Complex):
			a = self.real
			b = self.imag
			c = o.real
			d = o.imag
			num = c * c + d * d
			new_complex = Complex((a * c + b * d)/num, (b * c - a * d)/num)
			return new_complex
		else:
			print("Bad input in truediv function")
			return None

	def __rtruediv__(self, o):
		if isinstance(o, int) or isinstance(o, float):
			a = o
			c = self.real
			d = self.imag
			num = c * c + d * d
			new_complex = Complex((a * c)/num, (- a * d)/num)
			return new_complex
		elif isinstance(o, Complex):
			a = o.real
			b = o.imag
			c = self.real
			d = self.imag
			num = c * c + d * d
			new_complex = Complex((a * c + b * d)/num, (b * c - a * d)/num)
			return new_complex
		else:
			print("Bad input in rtruediv function")
			return None

	def __pow__(self, n):
		if isinstance(n, int):
			if n == 0:
				new_complex = Complex(1, 0)
				return new_complex
			new_complex = Complex(self.real, self.imag)
			new_complex2 = Complex(self.real, self.imag)
			for i in range(1, n):
				new_complex = new_complex * new_complex2
			return new_complex
		else:
			print("Bad input in pow function")
			return None

	def __rpow__(self, o):
		print("Bad input to power function")
		return None

	def __neg__(self):
		new_complex = Complex(- self.real, - self.imag)
		return new_complex