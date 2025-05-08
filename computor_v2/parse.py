from rational import Rational
from complex import Complex
from matrix import Matrix, Vector
from function import Term, Polynomial
from lexer import tokenize, parse_tokens, extract_matrix_literal, parse_matrix_literal

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

def parse_cmd(cmd):
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
	print(tokens)
	func = parse_tokens(tokens)
	print(func)

	func_def = 0
	if func and func[0] and func[0][0] == 'FUNC':
		func_def = 1

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
			print("assigning variable", tokens[0])
			print("equal to", tokens[2:])
			# here parse RHS
			return key, value

	# next check for functions
	if func_def:
		if func[len(func) - 1] != '=':
			if func[0][1] == 'i':
				print("ERROR: Assignment to i is forbidden")
				return None, None
			print("assigning function", func[0][1], " of ", func[0][2])
			print("equal to", func[2:])
			# here parse RHS, and terms[0][2] if necessary
			return key, value

	return key, value