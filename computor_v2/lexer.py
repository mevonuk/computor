import re
from matrix import Matrix, Vector
from rational import Rational
from complex import Complex
from variable import Variable
from polynomial import Term, Polynomial
from function import Function
from tree import Node
from lex_base import tokenize, parse_tokens

#if parsing a matix
def extract_matrix_literal(s):
	pattern = r'\[\[.*?\]\]'  # non-greedy match for matrix
	matches = re.findall(pattern, s)
	matrix_type = 2 # matrix type
	if not matches:
		pattern = r'\[.*?\]'  # non-greedy match for matrix
		matches = re.findall(pattern, s)
		matrix_type = 1 # vector type
	if not matches:
		matrix_type = 0 # not a matrix or vector type
	return matches, matrix_type

def split_terms(s):
	return re.findall(r'[+-]?\s*[^+-]+', s)

def parse_number(token):
	token = token.replace(' ', '')
	if token and token[0] not in ('+', '-'):
		token = '+' + token
	terms = split_terms(token)
	imag = 0
	real = 0
	for term in terms:
		if 'i' in term:
			term = term.replace('i', '')
			if not term or term == '+':
				imag += 1
			elif term == '-':
				imag -= 1
			elif '.' in term:
				imag += float(term)
			else:
				imag += int(term)
		else:
			if '.' in term:
				real += float(term)
			else:
				real += int(term)
	if imag != 0:
		return Complex(real, imag)
	else:
		return Rational(real)
	
def parse_matrix_literal(matrix_str, matrix_type):
	# Remove outer brackets
	rows = matrix_str.split(';')
	# remove brackets
	num_col = -1
	matrix_data = []
	for row in rows:
		row = row.replace('[','')
		row = row.replace(']','')
		new_row = []
		for term in row.split(','):
			term = term.strip()
			# parse term here
			term = parse_number(term)
			new_row.append(term)
		num_col_old = num_col
		num_col = len(new_row)
		if num_col_old != -1 and num_col_old != num_col:
			print("Error: All rows(col) of a matrix should have the same length")
			return None
		matrix_data.append(new_row)
	if matrix_type == 2:
		return Matrix(matrix_data)
	else:
		return Vector(matrix_data)


def parse_num(token):
	if isinstance(token, (Node, Complex, Rational, Variable)):
		return token
	if token == 'i':
		return Complex(0, 1)
	if token.isalpha():
		return Variable(token, None)
	if '.' in token:
		return Rational(float(token))
	else:
		return Rational(int(token))
	
precedence = {
	'**': 4,
	'^': 4,
	'*': 3,
	'/': 3,
	'%': 3,
	'+': 2,
	'-': 2,
	'=': 1
}

right_associative = {'^', '**'}

def parse_expression(tokens, index=0, min_precedence=1):
	def parse_primary(index):
		token = tokens[index]

		# Parentheses
		if token == '(':
			node, new_index = parse_expression(tokens, index + 1)
			if tokens[new_index] != ')':
				raise SyntaxError("Unmatched parenthesis")
			return node, new_index + 1

		# Function call tuple: ('FUNC', 'f', [['a']])
		elif isinstance(token, tuple) and token[0] == 'FUNC':
			func_name = token[1]
			args_token_lists = token[2]

			if len(args_token_lists) != 1:
				raise NotImplementedError("Only single-argument functions supported")

			arg_expr, _ = parse_expression(args_token_lists[0])
			#return Node(func_name, arg_expr, 'FUNC'), index + 1
			func = f"{func_name}({arg_expr})"
			return Node(func, None, 'FUNC'), index + 1

		return Node(parse_num(token), None, 'VAR'), index + 1

	lhs, index = parse_primary(index)

	while index < len(tokens):
		op = tokens[index]
		if op not in precedence:
			break
		prec = precedence[op]
		if prec < min_precedence:
			break
		next_min_prec = prec + (0 if op in right_associative else 1)

		rhs, index = parse_expression(tokens, index + 1, next_min_prec)

		lhs = Node(parse_num(lhs), parse_num(rhs), op)

	return lhs, index