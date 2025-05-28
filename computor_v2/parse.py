from rational import Rational
from complex import Complex
from matrix import Matrix, Vector
from polynomial import Term, Polynomial, RationalExpression, plug_in_var, sub_exprs
from function import Function
from lex_base import tokenize, parse_tokens, extract_matrix_literal, parse_matrix_literal
from lexer import parse_expression, parse_num
from tree import Node
from tools import get_value, get_value2
import re
from my_math_tools import quadratic

def check_equal_signs(s):
	# check number of = signs
	count = s.count('=')
	if count != 1:
		print("Error: Equation should have 1 equal sign.")
		return 1
	return 0

def check_decimals(s):
	# check multiple . in one term
	s_list = list(s)
	for i, c in enumerate(s_list):
		if c == '.':
			if i + 1 < len(s_list):
				sub_list = s_list[i + 1:]
				for cc in sub_list:
					if cc == '.':
						print("Error: Bad input, check decimal points.")
						return 1
					if not cc.isdigit():
						break
	return 0

def check_new_term(s):
	# check spaces to see if a new term starts
	s_list = list(s)
	for i, c in enumerate(s_list):
		if c.isdigit() or c == '.' or c.isalpha() or c == ')':
			if i + 1 < len(s_list) and  s_list[i + 1] == ' ':
				if i + 2 < len(s_list):
					sub_list = s_list[i + 2:]
					for cc in sub_list:
						if cc in set('+-=(*/%'): #these things indicate a new term
							break
						if cc.isdigit() or cc.isalpha():
							print("Error: Poorly written term")
							return 1
	return 0

def insert_mult(s):
    # Insert * between:
    # - number or variable and variable or opening parenthesis
    s = re.sub(r'(?<=[0-9a-zA-Z\)])\s+(?=[a-zA-Z\(])', ' * ', s)
    return s
							
# check user input
def check_input_chars(s):
	# check for allowed characters
	for c in s:
		if not c.isalpha() and not c.isdigit() and c not in set('+-/*^% ()=?.;[],'):
			print("Error: Not an allowed char:", c)
			return 1
	return 0

def count_paren(s):
	# check number of parentheses
	count1 = s.count('(')
	count2 = s.count(')')
	if count1 != count2:
		print("Error: Parentheses are not balanced")
		return 1
	# check number of brakets
	count1 = s.count('[')
	count2 = s.count(']')
	if count1 != count2:
		print("Error: Brackets are not balanced")
		return 1
	return 0

def split_at_equals(tokens):
    if '=' in tokens:
        idx = tokens.index('=')
        left = tokens[:idx]
        right = tokens[idx + 1:]
        return left, right
    else:
        raise ValueError("'=' not found in token list")

def define_function_terms(name, var, term):

	terms, _ = parse_expression(term)

	# if not isinstance(terms, Node):
		# terms = Node(terms, 0, 'FUNC')

	value = Function(name, var, terms)
	# here parse RHS, and terms[0][2] if necessary
	# print("key", key, "terms", terms)
	poly = value.convert_function()
	value = poly
	if isinstance(poly, RationalExpression):
		simplify = poly.simplify()
		print(simplify.solve(history))
		value = simplify
	return value

def define_function(func):
	var, _ = parse_expression(func[0][2])

	key = func[0][1]
	value = define_function_terms(func[0][1], var, func[2:])
	return key, value

def parse_cmd(cmd, history):
	cmd = cmd.lower()

	# remove all spaces
	# cmd = cmd.replace(" ", "")

	if not isinstance(cmd, str):
		print("Error: Bad input to parcer, not a string")
		return None, None
	
	if check_input_chars(cmd) == 1:
		return None, None
	if check_equal_signs(cmd) == 1:
		return None, None
	if check_decimals(cmd) == 1:
		return None, None

	# cmd = insert_mult(cmd)
	# print(cmd)

	if check_new_term(cmd) == 1:
		return None, None
	if count_paren(cmd) == 1:
		return None, None
	
	key = None
	value = None

	tokens = tokenize(cmd)
	func = parse_tokens(tokens)

	func_def = 0
	if func and func[0] and func[0][0] == 'FUNC':
		func_def = 1

	# check for solving, not FUNC
	if tokens[len(tokens) - 1] == '?' and func_def == 0:
		# remove = and ?
		end = len(tokens)-2
		tokens = tokens[:end]
		tokens = parse_tokens(tokens)

		tree, _ = parse_expression(tokens)
		if isinstance(tree, str):
			sol = get_value2(tree, history)
			# if not (isinstance(sol, Rational or isinstance(sol, Complex))):
			# 	sol = sol.solve_node(history)
			if isinstance(sol, Node):
				sol = sol.solve_node(history)
		else:
			sol = tree.solve_node(history)
		if sol != None:
			print(sol)
		return key, value

	# check for solving, FUNC
	if tokens[len(tokens) - 1] == '?' and func_def == 1:
		# remove ?
		end = len(tokens)-1
		tokens = tokens[:end]

		# case 1: ending with =
		if tokens[len(tokens)-1] == '=':
			# simple solve
			function = get_value(func[0][1], history)

			if function is None:
				print("Error: function is not defined")
				return key, value

			# check for variable
			variable = parse_num(func[0][2][0])
			if isinstance(function, (Polynomial, RationalExpression)):
				sol = plug_in_var(function, variable, history)
				print(sol)
			elif isinstance(variable, str):
				print(function, type(function))
				sol = function.terms.solve_node(history)
				print(sol)
			else:
				print("function not poly/rational or otherwise")

		# case 2: ending with  a number
		else:
			# quadratic solve
			# print("case 2: solve quadratic equation")
			left, right = split_at_equals(tokens)

			left = parse_tokens(left)
			right = parse_tokens(right)

			function_left = get_value(left[0][1], history)

			if function_left is None:
				print("Error: function is not defined")
				return key, value

			# this only works for the case of constant !!!
			var = next(iter(function_left.terms))[0]
			function_right = define_function_terms('dummy_function', var, right)

			print(function_left, '=', function_right)

			function = sub_exprs(function_left, function_right)

			degree = function.get_degree()
			
			if degree < 3 and degree >= 0:
				print("solving quadratic equation:", function, '= 0')
				a, b, c = function.get_coefficients(2)
				if isinstance(a, Rational):
					a = a.real
				if isinstance(b, Rational):
					b = b.real
				if isinstance(c, Rational):
					c = c.real
				quadratic(a, b, c)
			else:
				print("cannot solve equation", function, '= 0')

		return key, value

	# first check for matrices/vectors
	mat, mat_type = extract_matrix_literal(cmd)
	if mat and mat_type != 0:
		if not func_def:
			print("Found matrix, parsing...")
			key = tokens[0]
			matrix_input = parse_matrix_literal(mat[0], mat_type)
			value = matrix_input
			return key, value
		else:
			print("ERROR: assigning matrix/vector to function")
			return None, None
		
	# next check for regular variables
	if not func_def and tokens[0].isalpha() and tokens[1] == '=':
		if tokens[len(tokens) - 1] != '=':
			if tokens[0] == 'i':
				print("ERROR: Assignment to i is forbidden")
				return None, None

			# need to check for case where variable is set to itself plus something
			if tokens[0] in tokens[2:]:
				print("attempt to make variable recursive forbidden")
				return None, None

			# here parse RHS
			key = tokens[0]
			tokens = parse_tokens(tokens[2:])
			tree, _ = parse_expression(tokens)
			return key, tree

	# next check for functions
	if func_def:
		if func[len(func) - 1] != '=':
			if func[0][1] == 'i':
				print("ERROR: Assignment to i is forbidden")
				return None, None
			key, value = define_function(func)
			print(value)
			return key, value

	return key, value