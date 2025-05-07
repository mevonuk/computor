from rational import Rational
from complex import Complex
from matrix import Matrix, Vector

# Note: polynomial can only have one var, when solving for that var, 
# otherwise it should be possible (for plugging in the value)

# Modulo (%) is not allowed for Complex numbers

# each term of a polynomial is a coefficient multiplied by a variable to an exp
class Term:

    def __init__(self, coefficient, var, exp, operator):
        if isinstance(exp, int) and exp >= 0:
            self.exp = exp
        else:
            print("Usage Term: Exponent must be integer >= 0", exp)
            exit()
        if isinstance(coefficient, int) or isinstance(coefficient, float) or isinstance(coefficient, Rational) or isinstance(coefficient, Complex):
            self.coef = coefficient
        else:
            print("Usage Term: Coef must be int, float, rational, or complex", coefficient)
            exit()
        if isinstance(var, str):
            self.var = var
        else:
            print("Usage Term: Variable must be a string", var)
            exit()
        if operator in ('+', '-', '*', '%', '/'):
            self.op = operator

    def __repr__(self):
        varible = f"{self.var}^{self.exp}"
        if self.exp == 0:
            varible = ""
        if self.exp == 1:
            varible = f"{self.var}"
        if isinstance(self.coef, Complex) and self.coef.imag != 0:
            if self.exp == 0:
                return f"{self.coef}"
            else:
                return f"({self.coef}){varible}"
        else:
            if self.coef == 1:
                return f"{varible}"
            elif self.coef == -1:
                return f"-{varible}"
            else:
                return f"{self.coef}{varible}"

class Polynomial:
    def __init__(self):
        self.terms = {}  # key = exponent, var, value = coefficient, operator

    def add_term(self, *args):
        largs = list(args)
        if len(largs) != 1:
            print("Usage: add term with Term or 4-tuple")
            exit()
        if isinstance(largs[0], Term):
            term = largs[0]
        elif isinstance(largs[0], tuple):
            term = Term(*largs[0])
        else:
            print("Usage: add Term with Term or 4-tuple")
            exit()

        key = (term.var, term.exp)
        if key in self.terms:
            existing_coef, _ = self.terms[key]
            if term.op == '+':
                self.terms[key] = [existing_coef + term.coef, '+']
            elif term.op == '-':
                self.terms[key] = [existing_coef - term.coef, '+']
            elif term.op == '/':
                self.terms[key] = [existing_coef / term.coef, '+']
            elif term.op == '*':
                self.terms[key] = [existing_coef * term.coef, '+']
            elif term.op == '%':
                if not isinstance(existing_coef, Complex) and not isinstance(term.coef, Complex):
                    self.terms[key] = [existing_coef % term.coef, '+']
                else:
                    print("Error: mod operator not allowed with complex numbers")
                    exit()
        else:
            self.terms[key] = [term.coef, term.op]

    def __repr__(self):
        if not self.terms:
            return "0"
        function_terms = self.terms.items()
        parts = []
        for i, ((var, exp), (coef, op)) in enumerate(function_terms):
            if coef == 0:
                continue
            if isinstance(coef, Complex) and coef.imag != 0:
                term = Term(coef, var, exp, op)
            else:
                term = Term(abs(coef.real), var, exp, op)
            term_str = str(term)
            if i == 0:
                # First term: include sign only if negative
                if not isinstance(coef, Complex) and coef < 0:
                    parts.append(f"-{term_str}")
                elif isinstance(coef, Complex) and coef.imag == 0 and coef.real < 0:
                    parts.append(f"-{term_str}")
                else:
                    parts.append(f"{term_str}")
            else:
                # Subsequent terms: prepend with + or -
                if not isinstance(coef, Complex) and coef < 0:
                    parts.append(f" - {term_str}")
                elif isinstance(coef, Complex) and coef.imag == 0 and coef.real < 0:
                    parts.append(f" - {term_str}")
                else:
                    parts.append(f" + {term_str}")
        result = "".join(parts)
        if result:
            return result
        else:
            return '0'
        
    def plug_in_var(self, var, value):
        if not (isinstance(value, str) or isinstance(value, int) or isinstance(value, float) or isinstance(value, Rational) or isinstance(value, Complex)):
            print("Error: Currently value must be a number or str")
            exit()
        if not isinstance(var, str):
            print("Error: Variable name should be a string")
            exit()
        if var == "dummy_var":
            print("Error: use of the variable name dummy_var is forbidden")
            exit()

        keys_to_replace = []
        for (v, exp) in self.terms:
            if v == var:
                keys_to_replace.append((v, exp))

        for key in keys_to_replace:
            coef, op = self.terms.pop(key)
            if not isinstance(value, str):
                new_value = coef * (value ** key[1])
                self.add_term((new_value, 'dummy_var', 0, '+'))
            else:
                self.add_term((coef, value, key[1], op))