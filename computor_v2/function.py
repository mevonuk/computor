# contains Function class with routine to convert Function to Polynomial

from rational import Rational
from complex import Complex
from node import Node
from variable import Variable
from polynomial import Polynomial, RationalExpression, Term

from polynomial import mul_exprs, sub_exprs, add_exprs


class Function:
    """definition of function class
    holds name of function,
    variable that function is function of,
    and terms of function"""

    def __init__(self, name, variable, terms):
        """Initializes function"""
        if not isinstance(variable, (str, Node, Variable)):
            raise TypeError("Error: variable name should be a string or Node")
        if not isinstance(name, str):
            raise TypeError("Error: function name should be a string")
        ALLOWED_TYPES = (int, float, Node, Complex, Rational, Variable)
        if not isinstance(terms, ALLOWED_TYPES):
            raise TypeError("Error: function terms in bad type")
        if isinstance(variable, Node):
            variable = variable.left
        self.terms = terms
        self.var = variable
        self.name = name

    def __str__(self):
        """Instruction on how to convert function to string"""
        return f"{self.name}({self.var})"

    def convert_function(self):
        """Convert function to polynomial"""
        polynomial = self._node_to_polynomial(self.terms)
        return polynomial

    def _node_to_polynomial(self, node):
        """Convert terms to polynomial"""
        if isinstance(node, (int, float, Complex, Rational)):
            p = Polynomial()
            p.add_term((node, self.var, 0, '+'))
            return p

        # here need to make sure using only variable name !!!
        if isinstance(node, (str, Variable)):
            p = Polynomial()
            if isinstance(node, Variable) and node.name != self.var.name:
                p.add_term((node, self.var, 0, '+'))
            elif isinstance(node, str) and node != self.var.name:
                p.add_term((node, self.var, 0, '+'))
            else:
                p.add_term((1, self.var, 1, '+'))
            return p

        if node is None:
            # print("in node to polynomial: node is none")
            return

        if isinstance(node, Node):
            left = self._node_to_polynomial(node.left)
            right = self._node_to_polynomial(node.right)

            if node.type == 'VAR':
                return left

            if node.type == '+':
                return add_exprs(left, right)
            elif node.type == '-':
                return sub_exprs(left, right)
            elif node.type == '*':
                return mul_exprs(left, right)
            elif node.type == '/':
                if not isinstance(left, Polynomial):
                    print("Polynomials only in rational expressions")
                    return self
                if not isinstance(right, Polynomial):
                    print("Polynomials only in rational expressions")
                    return self
                return RationalExpression(left, right)
            elif node.type == '^':
                nr = node.right
                if isinstance(nr, int):
                    power = nr
                elif isinstance(nr, Rational) and nr.real % 1 == 0:
                    power = int(nr.real)
                elif isinstance(nr, Node):
                    hold = nr.left
                    if isinstance(hold, int):
                        power = hold
                    elif isinstance(hold, Rational) and hold.real % 1 == 0:
                        power = hold.real
                else:
                    print("Exponent must be an integer.", nr, type(nr))
                    return self
                base = self._node_to_polynomial(node.left)
                result = base
                for _ in range(power - 1):
                    result = result * base
                return result
            elif node.type == '%':
                result = Polynomial()
                result.add_term(Term(Node(left, right, '%'), self.var, 0, '+'))
                return result
            else:
                print(f"Unsupported operation {node.type}")
                return self

        print("Unhandled node type in polynomial conversion.")
        return self
