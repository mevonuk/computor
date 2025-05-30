from complex import Complex
from variable import Variable
from tools import get_value2

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
	
	def solve_node(self, history):
		left_value = self.left
		right_value = self.right
		# print("in solve_node", left_value, type(left_value), right_value, type(right_value), self.type)
		if isinstance(self.left, Node):
			left_value = self.left.solve_node(history)
		if isinstance(self.right, Node):
			right_value = self.right.solve_node(history)
		if isinstance(self.left, str):
			left_value = get_value2(self.left, history)
		if isinstance(self.right, str):
			right_value = get_value2(self.right, history)
		if isinstance(self.left, Variable):
			left_value = get_value2(self.left.name, history)
		if isinstance(self.right, Variable):
			right_value = get_value2(self.right.name, history)

		# print("in solve_node", left_value, type(left_value), right_value, type(right_value), self.type)

		if (left_value == None or right_value == None) and self.type != 'FUNC' and self.type != 'VAR':
			print("Equation cannot be resolved")
			return None

		if isinstance(left_value, str) or isinstance(right_value, str):
			return None

		if self.type == 'VAR' and right_value == None:
			return left_value

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