# definition of Term, Polynomial, and RationalExpression classes
# contains routines: mul_exprs, sub_exprs, sub_rational_exprs,
#                    add_exprs, add_rational_exprs, plug_in_var
from copy import deepcopy
from rational import Rational
from complex import Complex
from variable import Variable
from node import Node
from matrix import Matrix, Vector

from tools import get_value2
from tree_functions import simplify_node, resolve
from tree_tool import solve_node


def mul_exprs(a, b):
    """Rules for multiplying Polynominals and Rational Expressions"""
    if isinstance(a, Polynomial) and isinstance(b, Polynomial):
        return a * b
    elif isinstance(a, Polynomial) and isinstance(b, RationalExpression):
        new_num = a * b.numerator
        return RationalExpression(new_num, b.denominator)
    elif isinstance(a, RationalExpression) and isinstance(b, Polynomial):
        new_num = a.numerator * b
        return RationalExpression(new_num, a.denominator)
    elif (isinstance(a, RationalExpression) and
            isinstance(b, RationalExpression)):
        new_num = a.numerator * b.numerator
        new_den = a.denominator * b.denominator
        return RationalExpression(new_num, new_den)
    else:
        print("Unsupported multiplication combination")
        return None


def sub_exprs(a, b):
    """Rules for subtracting Polynominals and Rational Expressions"""
    if isinstance(a, Polynomial) and isinstance(b, Polynomial):
        return a - b
    elif isinstance(a, Polynomial) and isinstance(b, RationalExpression):
        # Convert a to rational with denom 1
        a_rational = RationalExpression(a, Polynomial())
        a_rational.denominator.add_term((1, a.var, 0, '+'))
        return sub_rational_exprs(a_rational, b)
    elif isinstance(a, RationalExpression) and isinstance(b, Polynomial):
        dummy_poly = Polynomial()
        dummy_poly.add_term((1, a.var, 0, '+'))
        return sub_exprs(a, RationalExpression(b, dummy_poly))
    elif (isinstance(a, RationalExpression) and
            isinstance(b, RationalExpression)):
        return sub_rational_exprs(a, b)
    else:
        print("Unsupported subtraction combination")
        return None


def sub_rational_exprs(r1, r2):
    """Rule for subtracting Rational Expressions"""
    # a/b - c/d = (ad - bc) / bd
    new_num1 = r1.numerator * r2.denominator
    new_num2 = r2.numerator * r1.denominator
    new_num = new_num1 - new_num2
    new_den = r1.denominator * r2.denominator
    return RationalExpression(new_num, new_den)


def add_exprs(a, b):
    """Rules for adding Polynominals and Rational Expressions"""
    if isinstance(a, Polynomial) and isinstance(b, Polynomial):
        return a + b
    elif isinstance(a, Polynomial) and isinstance(b, RationalExpression):
        # Convert a to rational with denom 1
        a_rational = RationalExpression(a, Polynomial())
        a_rational.denominator.add_term((1, a.var, 0, '+'))
        return add_rational_exprs(a_rational, b)
    elif isinstance(a, RationalExpression) and isinstance(b, Polynomial):
        return add_exprs(b, a)
    elif (isinstance(a, RationalExpression) and
            isinstance(b, RationalExpression)):
        return add_rational_exprs(a, b)
    else:
        print("Unsupported addition combination")
        return None


def add_rational_exprs(r1, r2):
    """Rule for adding Rational Expressions"""
    # a/b + c/d = (ad + bc) / bd
    new_num1 = r1.numerator * r2.denominator
    new_num2 = r2.numerator * r1.denominator
    new_num = new_num1 + new_num2
    new_den = r1.denominator * r2.denominator
    return RationalExpression(new_num, new_den)


class Term:
    """each term of a polynomial is a coefficient
    multiplied by a variable to an exp"""

    def __init__(self, coefficient, var, exp, operator):
        """Initialize a Term with a 4-tuple"""
        if isinstance(exp, int) and exp >= 0:
            self.exp = exp
        else:
            raise TypeError("Usage Term: Exponent must be integer >= 0", exp)
        if isinstance(coefficient, (int, float, Rational, Complex, Node, Matrix)):
            self.coef = coefficient
        elif isinstance(coefficient, str):
            self.coef = Variable(coefficient, None)
        elif isinstance(coefficient, Variable):
            self.coef = coefficient
        else:
            raise TypeError("Usage Term: Problem with Coef type")
        if isinstance(var, str):
            self.var = var
        elif isinstance(var, Variable):
            self.var = var.name
        else:
            raise TypeError("Usage Term: Variable must be a string")
        if operator in ('+', '-', '*', '%', '/'):
            self.op = operator

    def __repr__(self):
        """How to represent a Term in a string"""
        varible = f"{self.var}^{self.exp}"
        if self.exp == 0:
            varible = ""
        if self.exp == 1:
            varible = f"{self.var}"
        if isinstance(self.coef, Node):
            if self.exp == 0:
                return f"{self.coef}"
            else:
                return f"({self.coef}) * {varible}"
        elif isinstance(self.coef, Variable):
            if self.exp == 0:
                return f"{self.coef}"
            else:
                return f"({self.coef}){varible}"
        elif isinstance(self.coef, Complex) and self.coef.imag != 0:
            if self.exp == 0:
                return f"{self.coef}"
            else:
                return f"({self.coef}){varible}"
        else:
            if self.coef == 1:
                if varible:
                    return f"{varible}"
                return "1"
            elif self.coef == -1:
                if varible:
                    return f"-{varible}"
                return "-1"
            else:
                return f"{self.coef}{varible}"


class Polynomial:
    """Class to define a Polynomial consisting of Terms"""

    def __init__(self):
        """Terms are empty by default and var set to dummy_var"""
        self.terms = {}  # key = exponent, var, value = coefficient, operator
        self.var = "dummy_var"

    def add_term(self, *args):
        """Add a Term to the Polynomial via Term or 4-tuple"""
        largs = list(args)
        if len(largs) != 1:
            raise TypeError("Usage: add term with Term or 4-tuple")
        if isinstance(largs[0], Term):
            term = largs[0]
        elif isinstance(largs[0], tuple):
            term = Term(*largs[0])
        else:
            raise TypeError("Usage: add Term with Term or 4-tuple")

        # keys correspond to the exponent and the variable
        key = (term.var, term.exp)
        self.var = term.var
        if key in self.terms:
            existing_coef, _ = self.terms[key]
            if term.op == '+':
                hold = Node(existing_coef, term.coef, '+')
                self.terms[key] = [hold, '+']
            elif term.op == '-':
                hold = Node(existing_coef, term.coef, '-')
                self.terms[key] = [hold, '+']
            elif term.op == '/':
                hold = Node(existing_coef, term.coef, '/')
                self.terms[key] = [hold, '+']
            elif term.op == '*':
                hold = Node(existing_coef, term.coef, '*')
                self.terms[key] = [hold, '+']
            elif term.op == '%':
                if (isinstance(term.coef, (int, float, Rational)) and
                        isinstance(term.var, str)):
                    mod_result = (
                        term.coef % get_value2(term.var, {})
                        if callable(get_value2)
                        else term.coef % 1
                    )
                elif (isinstance(term.coef, (int, float, Rational)) and
                        isinstance(term.var, Variable)):
                    mod_result = Node(term.coef, term.var, '%')
                elif (isinstance(term.coef, Variable) and
                        isinstance(term.var, (int, float, Rational))):
                    mod_result = Node(term.coef, term.var, '%')
                else:
                    mod_result = Node(term.coef, term.var, '%')
                self.terms[(term.var, 0)] = [mod_result, '+']
        else:
            if isinstance(term.coef, (Variable, Node, Matrix)):
                self.terms[key] = [term.coef, term.op]
            elif term.coef.real == -1:
                self.terms[key] = [-1, term.op]
            elif term.coef.real == 1:
                self.terms[key] = [1, term.op]
            self.terms[key] = [term.coef, term.op]

    def __repr__(self):
        """How to represent a Polynomial in string"""
        if not self.terms:
            return "0"
        function_terms = self.terms.items()

        if self.get_degree() == 0:
            sol = self.get_coefficients(0)[0]
            return f"{sol}"

        parts = []
        for i, ((var, exp), (coef, op)) in enumerate(function_terms):
            if coef == 0 or coef is None:
                continue

            if isinstance(coef, Variable):
                term = Term(coef.name, var, exp, op)
            elif isinstance(coef, (Node, str, Variable, Matrix)):
                if exp == 0:
                    term = f'{coef}'
                elif exp == 1:
                    term = f'{coef} * {var}'
                else:
                    term = f'{coef} * {var}^{exp}'
            elif isinstance(coef, Complex) and coef.imag != 0:
                term = Term(coef, var, exp, op)
            else:
                term = Term(abs(coef.real), var, exp, op)

            term_str = str(term)
            if i == 0:
                # First term: include sign only if negative
                if (not isinstance(coef, (Complex, Variable, Node, str, Matrix)) and
                        coef < 0):
                    parts.append(f"-{term_str}")
                elif (isinstance(coef, Complex) and coef.imag == 0 and
                        coef.real < 0):
                    parts.append(f"-{term_str}")
                else:
                    parts.append(f"{term_str}")
            else:
                # Subsequent terms: prepend with + or -
                if (not isinstance(coef, (Complex, Variable, Node, str, Matrix)) and
                        coef < 0):
                    parts.append(f" - {term_str}")
                elif (isinstance(coef, Complex) and
                        coef.imag == 0 and
                        coef.real < 0):
                    parts.append(f" - {term_str}")
                else:
                    parts.append(f" + {term_str}")
        result = "".join(parts)
        if result:
            return result
        else:
            return '0'

    def get_coefficients(self, degree):
        """Obtain the coefficient of a given term"""
        if not self.terms:
            return [0] * (degree + 1)

        var = next(iter(self.terms))[0]  # get any variable used
        return [
            self.terms.get((var, i), (0, '+'))[0]
            for i in reversed(range(degree + 1))
        ]

    def factor(self):
        """factor for cases of var^2"""
        a, b, c = self.get_coefficients(2)

        if not a:
            return [self]  # Not a factorable quadratic or not univariate

        discriminant = b ** 2 - 4 * a * c

        if discriminant.real < 0 or (discriminant.real ** 0.5) % 1 != 0:
            return [self]  # Can't factor nicely

        sqrt_d = int(discriminant.real ** 0.5)
        r1 = (-b.real + sqrt_d) // (2 * a.real)
        r2 = (-b.real - sqrt_d) // (2 * a.real)

        r1 = Rational(r1)
        r2 = Rational(r2)

        f1 = Polynomial()
        f2 = Polynomial()

        var = next(iter(self.terms))[0]

        f1.add_term((1, var, 1, '+'))
        f1.add_term((-r1, var, 0, '+'))

        f2.add_term((1, var, 1, '+'))
        f2.add_term((-r2, var, 0, '+'))

        if a != 1:
            a_term = Polynomial()
            a_term.add_term((a, var, 0, '+'))
            return [a_term, f1, f2]
        else:
            return [f1, f2]

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __sub__(self, other):
        """Overload to subtract Polynomials"""
        if not isinstance(other, Polynomial):
            if isinstance(other, (Rational, int, float)):
                other = Polynomial.from_constant(other, var=self.var)
            else:
                print("Subtraction only supported between Polynomials.")
                return NotImplemented

        result = Polynomial()

        # First, copy all terms from self
        for (var, exp), (coef, op) in self.terms.items():
            result.terms[(var, exp)] = [coef, op]

        # Then, add or combine terms from other
        for (var, exp), (coef, op) in other.terms.items():
            key = (var, exp)
            if key in result.terms:
                existing_coef, _ = result.terms[key]
                # Assume + when adding terms from different polynomials
                if isinstance(existing_coef, (Node, Matrix)) or isinstance(coef, (Node, Matrix)):
                    result.terms[key] = [Node(existing_coef, coef, '-'), '+']
                else:
                    result.terms[key] = [existing_coef - coef, '+']
            else:
                result.terms[key] = [-coef, op]
        return result

    def __add__(self, other):
        """Overload to add Polynomials"""
        if not isinstance(other, Polynomial):
            if isinstance(other, (Rational, int, float)):
                other = Polynomial.from_constant(other, var=self.var)
            else:
                print("Addition only supported between Polynomial instances.")
                return NotImplemented

        result = Polynomial()

        # First, copy all terms from self
        for (var, exp), (coef, op) in self.terms.items():
            result.terms[(var, exp)] = [coef, op]

        # Then, add or combine terms from other
        for (var, exp), (coef, op) in other.terms.items():
            key = (var, exp)
            if key in result.terms:
                existing_coef, _ = result.terms[key]
                # Assume + when adding terms from different polynomials
                if isinstance(existing_coef, (Node, Matrix)) or isinstance(coef, (Node, Matrix)):
                    result.terms[key] = [Node(existing_coef, coef, '+'), '+']
                else:
                    result.terms[key] = [existing_coef + coef, '+']
            else:
                result.terms[key] = [coef, op]

        return result

    def __mul__(self, other):
        """Overload to multiply Polynomials"""
        if not isinstance(other, Polynomial):
            if isinstance(other, (Rational, int, float)):
                other = Polynomial.from_constant(other, var=self.var)
            else:
                return NotImplemented

        result = Polynomial()

        for (var1, exp1), (coef1, op1) in self.terms.items():
            for (var2, exp2), (coef2, op2) in other.terms.items():
                if var1 == "dummy_var":
                    var1 = var2
                if var2 == "dummy_var":
                    var2 = var1
                if var1 == var2:
                    new_exp = exp1 + exp2
                    new_var = var1
                else:
                    raise TypeError("Polynomials have different variables")

                if isinstance(coef1, (Variable, Node)):
                    if coef2 == 1:
                        new_coef = coef1
                    else:
                        new_coef = Node(coef1, coef2, '*')
                elif isinstance(coef2, (Variable, Node)):
                    if coef1 == 1:
                        new_coef = coef2
                    else:
                        new_coef = Node(coef1, coef2, '*')
                else:
                    new_coef = coef1 * coef2

                result.add_term((new_coef, new_var, new_exp, '+'))

        return result

    def __truediv__(self, other):
        """Overload to divide Polynomials by non-Polynomials"""
        if not isinstance(other, Polynomial):
            if isinstance(other, (Rational, int, float)):
                other = Polynomial.from_constant(other, var=self.var)
            else:
                return NotImplemented

        result = Polynomial()

        for (var1, exp1), (coef1, op1) in self.terms.items():
            for (var2, exp2), (coef2, op2) in other.terms.items():
                if coef2 == 0:
                    raise ZeroDivisionError("Division by zero: polynomial.")

                if var1 == var2:
                    # Combine like variable powers (subtract for division)
                    new_exp = exp1 - exp2
                    new_var = var1
                else:
                    raise TypeError("Polynomials have different variables")

                new_coef = coef1 / coef2
                result.add_term((new_coef, new_var, new_exp, '+'))

        return result

    def __mod__(self, other):
        """Overload to find modulo of const Polynomials by non-Polynomials"""
        if not isinstance(other, Polynomial):
            if isinstance(other, (Rational, int, float)):
                other = Polynomial.from_constant(other, var=self.var)
            else:
                return NotImplemented

        if self.get_degree() == 0 and other.get_degree() == 0:
            first = self.get_coefficients(0)[0]
            second = other.get_coefficients(0)[0]
            try:
                m = first % second
            except TypeError:
                m = Node(first, second, '%')
            return m

        else:
            raise TypeError("Modulo for non-constant polynomials")
            return None

    @classmethod
    def from_constant(cls, value, var='dummy_var'):
        """Transform a constant into a Polynomial"""
        poly = cls()
        poly.add_term((value, var, 0, '+'))
        return poly

    def solve(self, history):
        """Solve a polynomial by plugging in values from history"""
        value = next(iter(self.terms))[0]  # get any variable used
        # check if var in history
        if isinstance(value, str):
            value = Variable(value, get_value2(value, history))
        if isinstance(value, Variable):
            value = Variable(value.name, get_value2(value.name, history))

        if value.value == self.var or value.value is None:
            return self

        result = Polynomial()
        if isinstance(value.value, (int, float, Rational, Complex)):
            # plug value into polynomial
            result = plug_in_var(self, value, history)
        return result

    def combine_like_terms(self):
        """Combine terms with same var^exp if possible"""
        combined = {}
        for (var, exp), (coef, op) in self.terms.items():
            key = (var, exp)
            if isinstance(coef, Node):
                coef = simplify_node(coef, {})
            if isinstance(coef, str):
                coef = float(coef)
            if key in combined:
                combined[key][0] += coef
            else:
                combined[key] = [coef, op]
        self.terms = combined

    def plug_vars(self, history):
        """Similar to solve, plug in variables in history"""
        result = Polynomial()
        result.var = self.var

        for (var, exp), (coef, op) in self.terms.items():

            # Resolve coefficient
            if isinstance(coef, str):
                new_coef = get_value2(coef, history)
            elif isinstance(coef, Variable):
                new_coef = get_value2(coef.name, history)
            elif isinstance(coef, Node):
                new_coef = simplify_node(coef, history)
            elif isinstance(coef, Matrix):
                new_matrix = []
                for i in range(coef.shape[0]):
                    lst = []
                    for k in range(coef.shape[1]):
                        value2 = resolve(coef.data[i][k], history)
                        if isinstance(value2, Polynomial):
                            value2 = value2.solve(history)
                        lst.append(value2)
                    new_matrix.append(lst)
                if len(new_matrix) == 1 or len(new_matrix[0]) == 1:
                    new_coef = Vector(new_matrix)  # return vector
                else:
                    new_coef = Matrix(new_matrix)  # return matrix
            else:
                new_coef = None

            if new_coef is None:
                new_coef = coef

            key = (var, exp)
            if key in result.terms:
                result.terms[key][0] += new_coef
            else:
                result.terms[key] = [new_coef, op]

        return result

    def get_degree(self):
        """Get maximum degree of Polynomial"""
        max_exp = 0
        for (var, exp), (coef, op) in self.terms.items():
            if exp > max_exp:
                max_exp = exp
        return max_exp


class RationalExpression:
    """Class to represent a Polynomial divided by a Polynomial"""

    def __init__(self, numerator, denominator):
        """Innitiate class assuming use of Polynomials"""
        if not isinstance(numerator, Polynomial):
            raise TypeError("Error: Numerator must be Polynomial")
        if not isinstance(denominator, Polynomial):
            raise TypeError("Error: Denominator must be Polynomial")
        self.numerator = numerator
        self.denominator = denominator
        self.var = numerator.var

    def __repr__(self):
        """How to represent RationalExpression as a string"""
        top = f"({self.numerator})"
        bot = f"({self.denominator})"
        if self.numerator.get_degree() == 0:
            top = f"{self.numerator}"
        if self.denominator.get_degree() == 0:
            bot = f"{self.denominator}"
        return f"{top} / {bot}"

    def __add__(self, other):
        """Instructions to add two RationalExpressions"""
        if isinstance(other, Polynomial):
            other = RationalExpression(other, Polynomial())
            other.denominator.add_term((1, self.var, 0, '+'))
        if isinstance(other, RationalExpression):
            new_num1 = self.numerator * other.denominator
            new_num2 = other.numerator * self.denominator
            new_num = new_num1 + new_num2
            new_den = self.denominator * other.denominator
            return RationalExpression(new_num, new_den)
        raise NotImplementedError("Unsupported addition: RationalExpression")

    def simplify(self):
        """Check the rational expression to see if terms can be cancelled"""
        num_factors = self.numerator.factor()
        den_factors = self.denominator.factor()

        # Cancel common factors
        i = 0
        while i < len(num_factors):
            nf = num_factors[i]
            for j, df in enumerate(den_factors):
                if nf.terms == df.terms:
                    num_factors.pop(i)
                    den_factors.pop(j)
                    i -= 1
                    break
            i += 1

        new_num = Polynomial.from_constant(1, var=self.var)
        for f in num_factors:
            new_num = new_num * f

        new_den = Polynomial.from_constant(1, var=self.var)
        for f in den_factors:
            new_den = new_den * f

        var = next(iter(new_den.terms))[0]

        if (len(new_den.terms) == 1 and
                (var, 0) in new_den.terms and
                new_den.terms[(var, 0)][0] == 1):
            return new_num  # Simplified to a polynomial

        return RationalExpression(new_num, new_den)

    def solve(self, history):
        """attempt to solve top and bottom of RationalExpression"""
        top = Polynomial()
        bottom = Polynomial()
        if isinstance(self.numerator, Polynomial):
            top = self.numerator.solve(history)
        if isinstance(self.denominator, Polynomial):
            bottom = self.denominator.solve(history)
        result = RationalExpression(top, bottom)
        return result

    def plug_vars(self, history):
        """attempt to plug vaariables into top and bottom"""
        top = Polynomial()
        bottom = Polynomial()
        if isinstance(self.numerator, Polynomial):
            top = self.numerator.plug_vars(history)
        if isinstance(self.denominator, Polynomial):
            bottom = self.denominator.plug_vars(history)
        result = RationalExpression(top, bottom)
        return result

    def combine_like_terms(self):
        """attempt to combine like terms in top and bottom"""
        if isinstance(self.numerator, Polynomial):
            self.numerator.combine_like_terms()
        if isinstance(self.denominator, Polynomial):
            self.denominator.combine_like_terms()


def plug_in_var(func, var, history):
    """Plug in the value of a the function/polynomial variable"""
    value = deepcopy(var)
    if isinstance(var, str):
        value = get_value2(var, history)
        value = Variable(var.name, value)
    if isinstance(var, Variable) and var.value is None:
        value = get_value2(var.name, history)

    # RationalExpression support
    if isinstance(func, RationalExpression):
        top = plug_in_var(func.numerator, value, history)
        bottom = plug_in_var(func.denominator, value, history)
        result = RationalExpression(top, bottom)
        return result

    # Polynomial support
    elif isinstance(func, Polynomial):
        result = Polynomial()
        for (var, exp), (coef, op) in func.terms.items():
            result.terms[(var, exp)] = [coef, op]

        var = next(iter(result.terms))[0]
        keys_to_replace = []
        for (v, exp) in result.terms:
            if v == var:
                keys_to_replace.append((v, exp))

        for key in keys_to_replace:
            coef, op = result.terms.pop(key)

            new_coef = coef
            # if the coefficient is a Node, plug into that Node
            if isinstance(coef, Node):
                new_coef = plug_in_var(coef, value, history)
                solved_coef = solve_node(new_coef, history)
                if solved_coef is not None:
                    new_coef = solved_coef
                if key[1] != 0:
                    new_value = new_coef * (value.value ** key[1])
                else:
                    new_value = new_coef
                result.add_term((new_value, func.var, 0, '+'))
            elif not isinstance(value.value, str):
                if not isinstance(new_coef, (str, Node, Matrix)):
                    new_value = new_coef * (value.value ** key[1])
                elif isinstance(new_coef, Matrix):
                    # recursive search in case of vector/matrix
                    new_matrix = []
                    for i in range(new_coef.shape[0]):
                        lst = []
                        for k in range(new_coef.shape[1]):
                            value2 = resolve(new_coef.data[i][k], history)
                            if isinstance(value2, Polynomial):
                                value2 = value2.solve(history)
                            lst.append(value2)
                        new_matrix.append(lst)
                    if len(new_matrix) == 1 or len(new_matrix[0]) == 1:
                        new_value = Vector(new_matrix)* (value.value ** key[1])  # return vector
                    else:
                        new_value = Matrix(new_matrix)* (value.value ** key[1])  # return matrix
                else:
                    new_value = Node(new_coef, value.value ** key[1], '*')
                result.add_term((new_value, func.var, 0, '+'))
            else:
                result.add_term((new_coef, value.value, key[1], op))

        return result

    # Node support (for things like 3 % y)
    elif isinstance(func, Node):
        left = plug_in_var(func.left, value, history)
        right = plug_in_var(func.right, value, history)
        return Node(left, right, func.type)

    # Variable or variable name
    elif isinstance(func, Variable):
        if isinstance(value, Variable) and func.name == value.name:
            return value
        return func
    elif isinstance(func, str) and func == value.name:
        return value
    
    elif isinstance(func, Matrix):
        # recursive search in case of vector/matrix
        new_matrix = []
        for i in range(func.shape[0]):
            lst = []
            for k in range(func.shape[1]):
                value2 = plug_in_var(func.data[i][k], value, history)
                lst.append(value2)
            new_matrix.append(lst)
        if len(new_matrix) == 1 or len(new_matrix[0]) == 1:
            result = Vector(new_matrix)  # return vector
        else:
            result = Matrix(new_matrix)  # return matrix
        return result

    return func
