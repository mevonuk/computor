from complex import Complex
from matrix import Matrix
from variable import Variable
from lex_base import tokenize, parse_tokens, parse_num_raw
from polynomial import Polynomial, RationalExpression, plug_in_var
from tools import get_value, get_value2

class Node:

	def __init__(self, left, right, type):
		# left and right can be anything, op defines how they relate to each other
		self.left = left
		self.right = right
		self.type = type

	def __str__(self):
		l = str(self.left)
		r = str(self.right)
		o = str(self.type)
		if isinstance(self.left, Complex) and self.left.imag != 0:
			l = f"({l})"
		if isinstance(self.right, Complex) and self.right.imag != 0:
			r = f"({r})"
		if isinstance(self.left, Node):
			l = f"({l})"
		if isinstance(self.right, Node):
			r = f"({r})"
		if self.type in set('+-') or self.type == '**':
			o = f" {self.type} "
		if self.type in set('*/%^'):
			o = f"{self.type}"
		if self.type == 'FUNC':
			return f"{l}"
		if self.type == 'VAR':
			return f"{l}"
		return l + o + r
	
	def sub_var_node(self, variable):
		if isinstance(self.left, Variable) and self.left == variable:
			self.left = variable.value
		elif isinstance(self.left, str) and self.left == variable.name:
			self.left = variable.value
		elif isinstance(self.left, Node):
			self.left.sub_var_node(variable)

		if isinstance(self.right, Variable) and self.right == variable:
			self.right = variable.value
		elif isinstance(self.right, str) and self.right == variable.name:
			self.right = variable.value
		elif isinstance(self.left, Node):
			self.right.sub_var_node(variable)


	def solve_node(self, history):
		left_value = self.left
		right_value = self.right
		# print("solve", left_value, right_value, self.type)
		if isinstance(self.left, Node):
			left_value = self.left.solve_node(history)
		if isinstance(self.right, Node):
			right_value = self.right.solve_node(history)
		if isinstance(self.left, str):
			left_value = get_value(self.left, history)
		if isinstance(self.right, str):
			right_value = get_value(self.right, history)

		if (left_value == None or right_value == None) and self.type != 'FUNC' :
			print("Equation cannot be resolved")
			return None

		if self.type == '+':
			return left_value + right_value
		if self.type == '-':
			return left_value - right_value
		if self.type == '*':
			return left_value * right_value
		if self.type == '/':
			return left_value / right_value
		if self.type == '%':
			return left_value % right_value
		if self.type == '^':
			return left_value ** right_value
		if self.type == '**':
			if isinstance(left_value, Matrix) and isinstance(right_value, Matrix):
				return right_value * left_value
			print("** can only be used with matrix multiplication")
			return None
		if self.type == 'FUNC':
			func = self.left

			tokens = tokenize(func)
			func = parse_tokens(tokens)

			function = get_value2(func[0][1], history)
			if func[0][1] == function:
				print("Error: function not defined")
				return None

			# check for variable
			variable = parse_num_raw(func[0][2][0])

			if isinstance(function, (Polynomial, RationalExpression)):
				sol = plug_in_var(function, variable, history)
				# this is such a hack!
				hack = f"{sol}"
				sol = parse_num_raw(hack)
			elif isinstance(variable, str):
				print(function, type(function))
				sol = function.terms.solve_node(history)
				print('not defined', sol)
			else:
				print("function not poly/rational or otherwise")
				return None

			return sol
			

	def simplify_node(self, history):
		left_value = self.left
		right_value = self.right
		print("simplify", left_value, right_value, self.type)
		if isinstance(self.left, Node):
			left_value = self.left.simplify_node(history)
		if isinstance(self.right, Node):
			right_value = self.right.simplify_node(history)
		if isinstance(self.left, str):
			left_value = get_value2(self.left, history)
		if isinstance(self.right, str):
			right_value = get_value2(self.right, history)

		print("values:", left_value, right_value, self.type)
		
		if not (isinstance(self.right, Node) or isinstance(self.left, Node)) and not (isinstance(self.right, str) or isinstance(self.left, str)):
			if self.type == '+':
				return left_value + right_value
			if self.type == '-':
				return left_value - right_value
			if self.type == '*':
				return left_value * right_value
			if self.type == '/':
				return left_value / right_value
			if self.type == '%':
				return left_value % right_value
			if self.type == '^':
				return left_value ** right_value
			if self.type == '**':
				if isinstance(left_value, Matrix) and isinstance(right_value, Matrix):
					return right_value * left_value
				print("** can only be used with matrix multiplication")
				return None
		if self.type == 'FUNC':
			func = f"{self.left}"
			func = self.left
			if isinstance(func, str):
				return get_value2(func, history)
			return func
		return Node(left_value, right_value, self.type)
