# contains Function class with function to convert to polynomial,
# and intructions for operations with polynomials/rational expressions:
#   mul_exprs, sub_exprs, sub_rational_exprs, add_exprs, add_rational_exprs

from rational import Rational
from complex import Complex
from tree import Tree
from variable import Variable
from polynomial import Polynomial, RationalExpression


def mul_exprs(a, b):
    """method for multiplying polynomials and rational expressions"""
    if isinstance(a, Polynomial) and isinstance(b, Polynomial):
        # print('mul_exprs polynomials')
        return a * b
    elif isinstance(a, Polynomial) and isinstance(b, RationalExpression):
        new_num = a * b.numerator
        return RationalExpression(new_num, b.denominator)
    elif isinstance(a, RationalExpression):
        if isinstance(b, Polynomial):
            new_num = a.numerator * b
            return RationalExpression(new_num, a.denominator)
        elif isinstance(b, RationalExpression):
            new_num = a.numerator * b.numerator
            new_den = a.denominator * b.denominator
            return RationalExpression(new_num, new_den)
    print("Unsupported multiplication combination")
    exit()


def sub_exprs(a, b):
    """method for subtracting polynomials and rational expressions"""
    if isinstance(a, Polynomial) and isinstance(b, Polynomial):
        return a - b
    elif isinstance(a, Polynomial) and isinstance(b, RationalExpression):
        # Convert a to rational with denom 1
        a_rational = RationalExpression(a, Polynomial())
        a_rational.denominator.add_term((1, 'dummy_var', 0, '+'))
        return sub_rational_exprs(a_rational, b)
    elif isinstance(a, RationalExpression):
        if isinstance(b, Polynomial):
            dummy_poly = Polynomial()
            dummy_poly.add_term((1, 'dummy_var', 0, '+'))
            return sub_exprs(a, RationalExpression(b, dummy_poly))
        elif isinstance(b, RationalExpression):
            return sub_rational_exprs(a, b)
    print("Unsupported subtraction combination")
    exit()


def sub_rational_exprs(r1, r2):
    """method for subtracting rational expressions"""
    # a/b - c/d = (ad - bc) / bd
    new_num1 = r1.numerator * r2.denominator
    new_num2 = r2.numerator * r1.denominator
    new_num = new_num1 - new_num2
    new_den = r1.denominator * r2.denominator
    return RationalExpression(new_num, new_den)


def add_exprs(a, b):
    """method for adding polynomials and rational expressions"""
    if isinstance(a, Polynomial) and isinstance(b, Polynomial):
        return a + b
    elif isinstance(a, Polynomial) and isinstance(b, RationalExpression):
        # Convert a to rational with denom 1
        a_rational = RationalExpression(a, Polynomial())
        a_rational.denominator.add_term((1, 'dummy_var', 0, '+'))
        return add_rational_exprs(a_rational, b)
    elif isinstance(a, RationalExpression):
        if isinstance(b, Polynomial):
            return add_exprs(b, a)
        elif isinstance(b, RationalExpression):
            return add_rational_exprs(a, b)
    print("Unsupported addition combination")
    exit()


def add_rational_exprs(r1, r2):
    """method for adding rational expressions"""
    # a/b + c/d = (ad + bc) / bd
    new_num1 = r1.numerator * r2.denominator
    new_num2 = r2.numerator * r1.denominator
    new_num = new_num1 + new_num2
    new_den = r1.denominator * r2.denominator
    return RationalExpression(new_num, new_den)


class Function:
    """definition of function class
    holds name of function,
    variable that function is function of,
    and terms of function"""

    def __init__(self, name, variable, terms):
        """Initializes function"""
        if not isinstance(variable, (str, Tree, Variable)):
            raise TypeError("Error: variable name should be a string or Tree")
        if not isinstance(name, str):
            raise TypeError("Error: function name should be a string")
        if not isinstance(terms, (Tree, Complex, Rational, Variable)):
            raise TypeError("Error: function terms should be a Tree type")
        if isinstance(variable, Tree):
            # print("convert variable type")
            variable = variable.left
            # print(variable, type(variable))
        self.terms = terms
        self.var = variable
        self.name = name

    def __str__(self):
        """Instruction on how to convert function to string"""
        # return f"Function {self.name}({self.var}) = {self.terms}"
        return f"{self.name}({self.var})"

    def convert_function(self):
        """Convert function to polynomial"""
        # print("Converting function tree to polynomial...")
        # print('in convert function', self.terms, type(self.terms))
        polynomial = self._node_to_polynomial(self.terms)
        # print('in function convert_function', polynomial)
        return polynomial

    def _node_to_polynomial(self, node):
        """Convert terms to polynomial"""
        # print('in conversion', node, type(node))
        if isinstance(node, (int, float, Complex, Rational)):
            p = Polynomial()
            # print('in case rational', node, self.var)
            p.add_term((node, self.var, 0, '+'))
            # print(p)
            return p

        # here need to make sure using only variable name !!!
        if isinstance(node, (str, Variable)):
            p = Polynomial()
            # print('in case variable', node.name, self.var)
            if node.name != self.var.name:
                # print('in node to poly for variable', node, self.var)
                p.add_term((node, self.var, 0, '+'))
            else:
                # print('in node to poly for var', self.var)
                p.add_term((1, self.var, 1, '+'))
            # print('in node to poly, retuning poly', p)
            return p

        # if isinstance(node, Variable):
        # 	p = Polynomial()
        # 	p.add_term((1, node.name, 1, '+'))
        # 	return p

        if node is None:
            # print("in node to polynomial: node is none")
            return

        if isinstance(node, Tree):
            left = self._node_to_polynomial(node.left)
            right = self._node_to_polynomial(node.right)

            # print('in node to poly, left, right', left, right)

            if node.type == 'VAR':
                # print('deeper in node to polynomial', left, type(left))
                return left

            if node.type == '+':
                return add_exprs(left, right)
            elif node.type == '-':
                return sub_exprs(left, right)
            elif node.type == '*':
                # print('multiplying', left, right, type(left), type(right))
                return mul_exprs(left, right)
            elif node.type == '/':
                if not isinstance(left, Polynomial):
                    if not isinstance(right, Polynomial):
                        print("Polynomials only in rational expressions")
                        exit()
                return RationalExpression(left, right)
            elif node.type == '^':
                nr = node.right
                if isinstance(nr, int):
                    power = nr
                elif isinstance(nr, Rational) and nr.real % 1 == 0:
                    power = int(nr.real)
                elif isinstance(nr, Tree):
                    hold = nr.left
                    if isinstance(hold, int):
                        power = hold
                    elif isinstance(hold, Rational) and hold.real % 1 == 0:
                        power = hold.real
                else:
                    print("Exponent must be an integer.", nr, type(nr))
                    exit()
                base = self._node_to_polynomial(node.left)
                result = base
                for _ in range(power - 1):
                    result = result * base
                return result
            else:
                print(f"Unsupported operation {node.type}")
                exit()

        print("Unhandled node type in polynomial conversion.")
        exit()
