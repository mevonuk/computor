from rational import Rational
from complex import Complex
from matrix import Matrix, Vector
from function import Term, Polynomial, Function
from lexer import tokenize, parse_tokens, extract_matrix_literal, parse_matrix_literal
from lexer import parse_expression, parse_num
from tree import get_value, Node

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

def parse_cmd(cmd, history):
	if not isinstance(cmd, str):
		print("Error: Bad input to parcer, not a string")
		return None, None
	
	if check_input_chars(cmd) == 1:
		return None, None
	if check_equal_signs(cmd) == 1:
		return None, None
	if check_decimals(cmd) == 1:
		return None, None
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
		print("Solve equation")
		# remove = and ?
		end = len(tokens)-2
		tokens = tokens[:end]
		tokens = parse_tokens(tokens)

		tree, _ = parse_expression(tokens)
		if isinstance(tree, str):
			sol = get_value(tree, history)
			if not (isinstance(sol, Rational or isinstance(sol, Complex))):
				sol = sol.solve_node(history)
		else:
			sol = tree.solve_node(history)
		if sol != None:
			print(sol)
		return key, value

	# check for solving, FUNC
	if tokens[len(tokens) - 1] == '?' and func_def == 1:
		print("Solve equation, func")
		# remove = and ?
		end = len(tokens)-2
		tokens = tokens[:end]
		tokens = parse_tokens(tokens)
		print(tokens)

		function = get_value(func[0][1], history)

		# check for variable
		variable = parse_num(func[0][2][0])
		if isinstance(variable, str):
			sol = function.terms.solve_node(history)
			print(sol)
		else:
			sol = function.plug_var(variable, history)
			print(sol)

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
			print("assigning function", func[0][1], " of ", func[0][2], type(func[0][2]))
			var, _ = parse_expression(func[0][2])
			terms, _ = parse_expression(func[2:])
			if not isinstance(terms, Node):
				terms = Node(terms, 0, 'FUNC')
			print("equal to", terms, type(terms))
			key =func[0][1]
			value = Function(func[0][1], var, terms)
			# here parse RHS, and terms[0][2] if necessary
			print("key", key, "terms", terms)
			return key, value

	return key, value