# contains only Complex class with operation overloads

from my_math_tools import abs
from matrix import Matrix  # covered only in multiplication


class Complex:
    """Class for complex numbers with real and imaginary parts"""

    def __init__(self, real_value, imag_value):
        """Initialize complex object with real and imag parts"""
        if not isinstance(real_value, (int, float)):
            raise TypeError("in complex, real value should be int/real")
        if not isinstance(imag_value, (int, float)):
            raise TypeError("in complex, imaginary value should be int/real")
        self.real = real_value
        self.imag = imag_value

    def __str__(self):
        """Convert complex object to string"""
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
        """Overload for addition of complex objects"""
        if isinstance(o, (int, float)):
            new_complex = Complex(self.real + o, self.imag)
            return new_complex
        elif isinstance(o, Complex):
            new_complex = Complex(self.real + o.real, self.imag + o.imag)
            return new_complex
        else:
            print("Bad input in complex add function")
            return None

    def __radd__(self, o):
        """Overload to reverse addition of complex objects"""
        if isinstance(o, (int, float)):
            new_complex = Complex(self.real + o, self.imag)
            return new_complex
        elif isinstance(o, Complex):
            new_complex = Complex(self.real + o.real, self.imag + o.imag)
            return new_complex
        else:
            print("Bad input in complex radd function")
            return None

    def __sub__(self, o):
        """Overload to subtraction of complex objects"""
        if isinstance(o, (int, float)):
            new_complex = Complex(self.real - o, self.imag)
            return new_complex
        elif isinstance(o, Complex):
            new_complex = Complex(self.real - o.real, self.imag - o.imag)
            return new_complex
        else:
            print("Bad input in complex sub function")
            return None

    def __rsub__(self, o):
        """Overload to reverse subtraction of complex objects"""
        if isinstance(o, (int, float)):
            new_complex = Complex(o - self.real, -self.imag)
            return new_complex
        elif isinstance(o, Complex):
            new_complex = Complex(-self.real + o.real, o.imag - self.imag)
            return new_complex
        else:
            print("Bad input in complex rsub function")
            return None

    def __mul__(self, o):
        """Overload to multiplication of complex objects"""
        if isinstance(o, (int, float)):
            new_complex = Complex(self.real * o, self.imag * o)
            return new_complex
        elif isinstance(o, Complex):
            a = self.real
            b = self.imag
            c = o.real
            d = o.imag
            new_complex = Complex(a * c - b * d, a * d + b * c)
            return new_complex
        elif isinstance(o, Matrix):
            return o * self
        else:
            print("Bad input in complex mul function")
            return None

    def __rmul__(self, o):
        """Overload to reverse multiplication of complex objects"""
        if isinstance(o, (int, float)):
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
            print("Bad input in complex rmul function")
            return None

    def __truediv__(self, o):
        """Overload to division of complex objects"""
        if isinstance(o, (int, float)):
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
            print("Bad input in complex truediv function")
            return None

    def __rtruediv__(self, o):
        """Overload to reverse division of complex objects"""
        if isinstance(o, (int, float)):
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
            print("Bad input in complex rtruediv function")
            return None

    def __pow__(self, n):
        """Overload for complex power function"""
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
            print("Bad input in complex pow function")
            return None

    def __rpow__(self, o):
        """Overload for reverse complex power function"""
        print("Bad input to complex power function")
        return None

    def __neg__(self):
        """Overload for complex negation function"""
        new_complex = Complex(- self.real, - self.imag)
        return new_complex
