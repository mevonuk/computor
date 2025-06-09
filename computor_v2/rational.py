# operations with Variable or Matrix not covered everywhere
from complex import Complex
from matrix import Matrix  # covered only in multiplication
from variable import Variable  # covered only in multiplication
from node import Node


class Rational(Complex):
    """Rational child class of Complex
    imaginary part is equal to zero"""

    def __init__(self, value):
        """Initialize Rational value"""
        if isinstance(value, (int, float)):
            Complex.__init__(self, value, 0)
        else:
            raise TypeError("Value is not rational")

    def __str__(self):
        """String prep of Rational"""
        return str(self.real)

    def __add__(self, o):
        """Overload of addition operator Rational"""
        if isinstance(o, (int, float)):
            new_rational = Rational(self.real + o)
            return new_rational
        elif isinstance(o, Rational):
            new_rational = Rational(self.real + o.real)
            return new_rational
        elif isinstance(o, Complex):
            new_complex = Complex(self.real + o.real, o.imag)
            return new_complex
        else:
            print("Bad input in add function rational", o, type(o))
            return None

    def __radd__(self, o):
        """Overload of r addition operator Rational"""
        if isinstance(o, (int, float)):
            new_rational = Rational(self.real + o)
            return new_rational
        elif isinstance(o, Rational):
            new_rational = Rational(self.real + o.real)
            return new_rational
        elif isinstance(o, Complex):
            new_complex = Complex(self.real + o.real, o.imag)
            return new_complex
        elif isinstance(o, Node):
            new_node = Node(self, o, '+')
            return new_node
        else:
            print("Bad input in r radd function rational", o, type(o))
            return None

    def __sub__(self, o):
        """Overload of subtraction operator Rational"""
        if isinstance(o, (int, float)):
            new_rational = Rational(self.real - o)
            return new_rational
        elif isinstance(o, Rational):
            new_rational = Rational(self.real - o.real)
            return new_rational
        elif isinstance(o, Complex):
            new_complex = Complex(self.real - o.real, -o.imag)
            return new_complex
        else:
            print("Bad input in r sub function rational")
            return None

    def __rsub__(self, o):
        """Overload of r subtraction operator Rational"""
        if isinstance(o, (int, float)):
            new_rational = Rational(o - self.real)
            return new_rational
        elif isinstance(o, Rational):
            new_rational = Rational(-self.real + o.real)
            return new_rational
        elif isinstance(o, Complex):
            new_complex = Complex(-self.real + o.real, o.imag)
            return new_complex
        else:
            print("Bad input in r rsub function rational")
            return None

    def __mul__(self, o):
        """Overload of multiplication operator Rational"""
        if isinstance(o, (int, float)):
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
            print("Bad input in r mul function rational")
            return None

    def __rmul__(self, o):
        """Overload of r multiplication operator Rational"""
        if isinstance(o, (int, float)):
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
            print("Bad input in r rmul function rational", o, type(o))
            return None

    def __truediv__(self, o):
        """Overload of division operator Rational"""
        if isinstance(o, (int, float)):
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
            print("Bad input in truediv function rational")
            return None

    def __rtruediv__(self, o):
        """Overload of r division operator Rational"""
        if isinstance(o, (int, float)):
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
            print("Bad input in r rtruediv function rational")
            return None

    def __mod__(self, o):
        """Overload of modulo operator Rational"""
        if isinstance(o, (int, float)):
            new_rational = Rational(self.real % o)
            return new_rational
        elif isinstance(o, Rational):
            new_rational = Rational(self.real % o.real)
            return new_rational
        elif isinstance(o, Complex) and o.imag == 0:
            new_rational = Rational(self.real % o.real)
            return new_rational
        else:
            print("Bad input in mod function rational")
            return None

    def __rmod__(self, o):
        """Overload of modulo operator Rational"""
        if isinstance(o, (int, float)):
            new_rational = Rational(o % self.real)
            return new_rational
        elif isinstance(o, Rational):
            new_rational = Rational(o.real % self.real)
            return new_rational
        elif isinstance(o, Complex) and o.imag == 0:
            new_rational = Rational(o.real % self.real)
            return new_rational
        else:
            print("Bad input in r rmod function rational")
            return None

    def __pow__(self, n):
        """Overload of power operator Rational"""
        if isinstance(n, (int, float)):
            new_rational = Rational(self.real ** n)
            return new_rational
        elif isinstance(n, Rational):
            new_rational = Rational(self.real ** n.real)
            return new_rational
        elif isinstance(n, Complex) and n.imag == 0:
            new_rational = Rational(self.real ** n.real)
            return new_rational
        else:
            print("Bad input in pow function rational")
            return None

    def __rpow__(self, n):
        """Overload of r power operator Rational"""
        if isinstance(n, (int, float)):
            new_rational = Rational(n ** self.real)
            return new_rational
        elif isinstance(n, Rational):
            new_rational = Rational(n.real ** self.real)
            return new_rational
        elif isinstance(n, Complex) and n.imag == 0:
            new_rational = Rational(n.real ** self.real)
            return new_rational
        else:
            print("Bad input in r rpow function rational")
            return None

    def __neg__(self):
        """Overload of negation operator Rational"""
        new_rational = Rational(- self.real)
        return new_rational

    def __eq__(self, other):
        """Overload of equality operator Rational"""
        if isinstance(other, (int, float)):
            if self.real == other:
                return True
        elif isinstance(other, Rational):
            if self.real == other.real:
                return True
        elif isinstance(other, Complex) and other.imag == 0:
            if self.real == other.real:
                return True
        return False
