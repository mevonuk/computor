# operations with Variable or Matrix not covered everywhere

from complex import Complex
from matrix import Matrix
from variable import Variable
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
        """String rep of Rational"""
        return str(self.real)

    def __repr__(self):
        """String rep of Rational"""
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
        elif isinstance(o, Variable):
            if o.value is not None:
                return o.value + self
            else:
                return Node(self, o, '+')
        else:
            return Node(o, self, '+')

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
        elif isinstance(o, Variable):
            if o.value is not None:
                return o.value + self
            else:
                return Node(self, o, '+')
        else:
            return Node(o, self, '+')

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
        elif isinstance(o, Variable):
            if o.value is not None:
                return self - o.value
            else:
                return Node(self, o, '-')
        else:
            return Node(self, o, '-')

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
        elif isinstance(o, Variable):
            if o.value is not None:
                return o.value - self
            else:
                return Node(o, self, '-')
        else:
            return Node(o, self, '-')

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
            if o.value is not None:
                return o.value * self
            else:
                return Node(self, o, '*')
        else:
            return Node(o, self, '*')

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
            if o.value is not None:
                return o.value * self
            else:
                return Node(self, o, '*')
        else:
            return Node(o, self, '*')

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
        elif isinstance(o, Variable):
            if o.value is not None:
                return self / o.value
            else:
                return Node(self, o, '/')
        else:
            return Node(self, o, '/')

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
        elif isinstance(o, Variable):
            if o.value is not None:
                return o.value / self
            else:
                return Node(o, self, '/')
        else:
            return Node(o, self, '/')

    def __mod__(self, o):
        """Overload of modulo operator Rational"""
        if isinstance(o, (int, float)):
            new_rational = Rational(self.real % o)
            return new_rational
        elif isinstance(o, Rational):
            new_rational = Rational(self.real % o.real)
            return new_rational
        elif isinstance(o, Complex):
            if o.imag == 0:
                new_rational = Rational(self.real % o.real)
                return new_rational
            else:
                print("Modulo not defined for complex numbers")
                return None
        elif isinstance(o, Variable):
            if o.value is not None:
                return self % o.value
            else:
                return Node(self, o, '%')
        else:
            return Node(self, o, '%')

    def __rmod__(self, o):
        """Overload of modulo operator Rational"""
        if isinstance(o, (int, float)):
            new_rational = Rational(o % self.real)
            return new_rational
        elif isinstance(o, Rational):
            new_rational = Rational(o.real % self.real)
            return new_rational
        elif isinstance(o, Complex):
            if o.imag == 0:
                new_rational = Rational(o.real % self.real)
                return new_rational
            else:
                print("Modulo not defined for complex numbers")
                return None
        elif isinstance(o, Variable):
            if o.value is not None:
                return o.value % self
            else:
                return Node(o, self, '%')
        else:
            return Node(o, self, '%')

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
        elif isinstance(n, Variable):
            if n.value is not None and isinstance(n.value, int):
                return self ** n.value
            else:
                return Node(self, n, '^')
        else:
            return Node(self, n, '^')

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
        elif isinstance(n, Variable):
            if n.value is not None:
                return n.value ** self
            else:
                return Node(n, self, '^')
        else:
            return Node(n, self, '^')

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
