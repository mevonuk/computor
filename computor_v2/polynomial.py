from rational import Rational
from complex import Complex
from tree import Node, get_value2
from variable import Variable

def mul_exprs(a, b):
	if isinstance(a, Polynomial) and isinstance(b, Polynomial):
		return a * b
	elif isinstance(a, Polynomial) and isinstance(b, RationalExpression):
		new_num = a * b.numerator
		return RationalExpression(new_num, b.denominator)
	elif isinstance(a, RationalExpression) and isinstance(b, Polynomial):
		new_num = a.numerator * b
		return RationalExpression(new_num, a.denominator)
	elif isinstance(a, RationalExpression) and isinstance(b, RationalExpression):
		new_num = a.numerator * b.numerator
		new_den = a.denominator * b.denominator
		return RationalExpression(new_num, new_den)
	else:
		print("Unsupported multiplication combination")
		exit()

def sub_exprs(a, b):
	if isinstance(a, Polynomial) and isinstance(b, Polynomial):
		return a - b
	elif isinstance(a, Polynomial) and isinstance(b, RationalExpression):
		# Convert a to rational with denom 1
		a_rational = RationalExpression(a, Polynomial())
		a_rational.denominator.add_term((1, 'dummy_var', 0, '+'))
		return sub_rational_exprs(a_rational, b)
	elif isinstance(a, RationalExpression) and isinstance(b, Polynomial):
		dummy_poly = Polynomial()
		dummy_poly.add_term((1, 'dummy_var', 0, '+'))
		return sub_exprs(a, RationalExpression(b, dummy_poly))
	elif isinstance(a, RationalExpression) and isinstance(b, RationalExpression):
		return sub_rational_exprs(a, b)
	else:
		print("Unsupported subtraction combination")
		exit()

def sub_rational_exprs(r1, r2):
	# a/b - c/d = (ad - bc) / bd
	new_num1 = r1.numerator * r2.denominator
	new_num2 = r2.numerator * r1.denominator
	new_num = new_num1 - new_num2
	new_den = r1.denominator * r2.denominator
	return RationalExpression(new_num, new_den)


def add_exprs(a, b):
	if isinstance(a, Polynomial) and isinstance(b, Polynomial):
		return a + b
	elif isinstance(a, Polynomial) and isinstance(b, RationalExpression):
		# Convert a to rational with denom 1
		a_rational = RationalExpression(a, Polynomial())
		a_rational.denominator.add_term((1, 'dummy_var', 0, '+'))
		return add_rational_exprs(a_rational, b)
	elif isinstance(a, RationalExpression) and isinstance(b, Polynomial):
		return add_exprs(b, a)
	elif isinstance(a, RationalExpression) and isinstance(b, RationalExpression):
		return add_rational_exprs(a, b)
	else:
		print("Unsupported addition combination")
		exit()

def add_rational_exprs(r1, r2):
	# a/b + c/d = (ad + bc) / bd
	new_num1 = r1.numerator * r2.denominator
	new_num2 = r2.numerator * r1.denominator
	new_num = new_num1 + new_num2
	new_den = r1.denominator * r2.denominator
	return RationalExpression(new_num, new_den)

class Function:

	def __init__(self, name, variable, terms):
		if not (isinstance(variable, str) or isinstance(variable, Node)):
			print("Error: variable name should be a string or node")
			exit()
		if not isinstance(name, str):
			print("Error: function name should be a string")
			exit()
		if not (isinstance(terms, Node) or isinstance(terms, Complex) or isinstance(terms, Rational)):
			print("Error: function terms should be a node type")
			exit()
		self.terms = terms
		self.var = variable
		self.name = name

	def __str__(self):
		#return f"Function {self.name}({self.var}) = {self.terms}"
		return f"{self.name}({self.var})"
	
	# def plug_var(self, value, history):
	# 	# this needs to be changed to not overwrite x permenently
	#     var = Variable(self.var, value)

	#     hold = self.terms
	#     hold.sub_var_node(var)

	#     return hold.solve_node(history)
	


	# here
	def convert_function(self):
		print("Converting function tree to polynomial...")
		polynomial = self._node_to_polynomial(self.terms)
		return polynomial

	def _node_to_polynomial(self, node):
		if isinstance(node, (int, float, Complex, Rational)):
			p = Polynomial()
			p.add_term((node, self.var, 0, '+'))
			return p

		if isinstance(node, str):
			p = Polynomial()
			p.add_term((1, node, 1, '+'))
			return p

		if isinstance(node, Variable):
			p = Polynomial()
			p.add_term((1, node.name, 1, '+'))
			return p

		if isinstance(node, Node):
			left = self._node_to_polynomial(node.left)
			right = self._node_to_polynomial(node.right)

			if node.type == '+':
				return add_exprs(left, right)
			elif node.type == '-':
				return sub_exprs(left, right)
			elif node.type == '*':
				return mul_exprs(left, right)
			elif node.type == '/':
				if not isinstance(left, Polynomial) or not isinstance(right, Polynomial):
					print("Only polynomial numerator and denominator supported in rational expressions")
					exit()
				return RationalExpression(left, right)
			elif node.type == '^':
				if isinstance(node.right, int):
					power = node.right
				elif isinstance(node.right, Rational) and node.right.real % 1 == 0:
					power = int(node.right.real)
				else:
					print("Exponent must be an integer.")
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
		if isinstance(coefficient, (int, float, Rational, Complex)):
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
			if term.coef.real == -1:
				self.terms[key] = [-1, term.op]
			elif term.coef.real == 1:
				self.terms[key] = [1, term.op]
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
	
	def get_coefficients(self, degree):
		if not self.terms:
			return [0] * (degree + 1)

		var = next(iter(self.terms))[0]  # get any variable used
		return [
			self.terms.get((var, i), (0, '+'))[0]
			for i in reversed(range(degree + 1))
		]

	# factor for cases of var^2
	def factor(self):
		a, b, c = self.get_coefficients(2)

		if not a :
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

	def __sub__(self, other):
		if not isinstance(other, Polynomial):
			print("Subtraction only supported between Polynomial instances.")
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
				result.terms[key] = [existing_coef - coef, '+']
			else:
				result.terms[key] = [-coef, op]

		return result
	
	def __add__(self, other):
		if not isinstance(other, Polynomial):
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
				result.terms[key] = [existing_coef + coef, '+']
			else:
				result.terms[key] = [coef, op]

		return result

	def __mul__(self, other):
		if not isinstance(other, Polynomial):
			return NotImplemented

		result = Polynomial()

		for (var1, exp1), (coef1, op1) in self.terms.items():
			for (var2, exp2), (coef2, op2) in other.terms.items():
				if var1 == var2:
					# Combine like variable powers
					new_exp = exp1 + exp2
					new_var = var1
				elif var1 == "dummy_var":
					new_var = var2
					new_exp = exp2
				elif var2 == "dummy_var":
					new_var = var1
					new_exp = exp1
				else:
					print(f"Error: Cannot multiply polynomials with different variables ({var1}, {var2})")
					exit()

				new_coef = coef1 * coef2
				result.add_term((new_coef, new_var, new_exp, '+'))

		return result

	def __truediv__(self, other):
		if not isinstance(other, Polynomial):
			return NotImplemented

		result = Polynomial()

		for (var1, exp1), (coef1, op1) in self.terms.items():
			for (var2, exp2), (coef2, op2) in other.terms.items():
				if coef2 == 0:
					print("Error: Division by zero coefficient in polynomial term.")
					exit()

				if var1 == var2:
					# Combine like variable powers (subtract for division)
					new_exp = exp1 - exp2
					new_var = var1
				elif var1 == "dummy_var":
					new_var = var2
					new_exp = -exp2
				elif var2 == "dummy_var":
					new_var = var1
					new_exp = exp1
				else:
					print(f"Error: Cannot divide polynomials with different variables ({var1}, {var2})")
					exit()

				new_coef = coef1 / coef2
				result.add_term((new_coef, new_var, new_exp, '+'))

		return result

	@classmethod
	def from_constant(cls, value, var='dummy_var'):
		poly = cls()
		poly.add_term((value, var, 0, '+'))
		return poly

	def solve(self, history):
		var = next(iter(self.terms))[0]  # get any variable used
		# check if var in history
		value = get_value2(var, history)
		result = Polynomial()
		if isinstance(value, (int, float, Rational, Complex)):
			# plug value into polynomial
			result = plug_in_var(self, value)
		return result

	def get_degree(self):
		max_exp = 0
		for (var, exp), (coef, op) in self.terms.items():
			if exp > max_exp:
				max_exp = exp
		return max_exp

class RationalExpression:
	def __init__(self, numerator, denominator):
		if not isinstance(numerator, Polynomial) or not isinstance(denominator, Polynomial):
			print("Error: Both numerator and denominator must be Polynomial instances")
			exit()
		self.numerator = numerator
		self.denominator = denominator

	def __repr__(self):
		top = f"({self.numerator})"
		bot = f"({self.denominator})"
		if self.numerator.get_degree() == 0:
			top = f"{self.numerator}"
		if self.denominator.get_degree() == 0:
			bot = f"{self.denominator}"
		if self.numerator.get_degree() == 0 and self.denominator.get_degree() == 0:
			return f"{self.numerator/self.denominator}"
		return f"{top} / {bot}"

	def __add__(self, other):
		if isinstance(other, Polynomial):
			other = RationalExpression(other, Polynomial())
			other.denominator.add_term((1, 'dummy_var', 0, '+'))
		if isinstance(other, RationalExpression):
			new_num1 = self.numerator * other.denominator
			new_num2 = other.numerator * self.denominator
			new_num = new_num1 + new_num2
			new_den = self.denominator * other.denominator
			return RationalExpression(new_num, new_den)
		print("Unsupported addition with RationalExpression")
		exit()

	# check if there are factors that can be cancelled out
	def simplify(self):
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

		new_num = Polynomial.from_constant(1)
		for f in num_factors:
			new_num = new_num * f

		new_den = Polynomial.from_constant(1)
		for f in den_factors:
			new_den = new_den * f

		var = next(iter(new_den.terms))[0]

		if len(new_den.terms) == 1 and (var, 0) in new_den.terms and new_den.terms[(var, 0)][0] == 1:
			return new_num  # Simplified to a polynomial
		return RationalExpression(new_num, new_den)

	def solve(self, history):
		# attempt to solve top and bottom
		top = Polynomial()
		bottom = Polynomial()
		if isinstance(self.numerator, Polynomial):
			top = self.numerator.solve(history)
		if isinstance(self.denominator, Polynomial):
			bottom = self.denominator.solve(history)
		result = RationalExpression(top, bottom)
		return result
		# print(self.numerator / self.denominator)

def plug_in_var(func, value):
	# attempt to solve top and bottom
	if isinstance(func, RationalExpression):
		print("plugging in value in rationalexp")
		top = Polynomial()
		bottom = Polynomial()
		if isinstance(func.numerator, Polynomial):
			top = plug_in_var(func.numerator, value)
		if isinstance(func.denominator, Polynomial):
			bottom = plug_in_var(func.denominator, value)
		result = RationalExpression(top, bottom)
		return result
		# print(self.numerator / self.denominator)
	elif isinstance(func, Polynomial):
		print("plugging in val in poly")
		if not isinstance(value, (str, int, float, Rational, Complex)):
			print("Error: Currently value must be a number or str")
			exit()

		result = Polynomial()

		# First, copy all terms from func
		for (var, exp), (coef, op) in func.terms.items():
			result.terms[(var, exp)] = [coef, op]


		var = next(iter(result.terms))[0]

		keys_to_replace = []
		for (v, exp) in result.terms:
			if v == var:
				keys_to_replace.append((v, exp))

		for key in keys_to_replace:
			coef, op = result.terms.pop(key)
			if not isinstance(value, str):
				new_value = coef * (value ** key[1])
				result.add_term((new_value, 'dummy_var', 0, '+'))
			else:
				result.add_term((coef, value, key[1], op))

		return result
	else:
		print("not a rational expression or poly, cannot plug_in_var")