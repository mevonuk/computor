from rational import Rational
from complex import Complex
from tree import Node
from tools import get_value2
from variable import Variable
from polynomial import Polynomial, RationalExpression, Term

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
	
	def convert_function(self):
		# print("Converting function tree to polynomial...")
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
