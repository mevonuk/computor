import re
from matrix import Matrix, Vector
from rational import Rational
from complex import Complex
from variable import Variable
from function import Term, Polynomial, Function
from tree import Node

def tokenize(expr):
    # Only insert * where it's clearly implied, not between a function name and (
    # Insert * between number and variable or (
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    # Insert * between ) and variable or number
    expr = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', expr)
    # Insert * between variable and another variable (e.g., x y → x*y)
    expr = re.sub(r'([a-zA-Z])\s+([a-zA-Z])', r'\1*\2', expr)
    # DO NOT insert * between variable and ( — that breaks function calls

    # Replace unary minus before variables (e.g., -x -> -1*x), but NOT before numbers
    expr = re.sub(r'(?<![\w\)])-(?=[a-zA-Z_])', r'-1*', expr)

    token_pattern = r'''
        (\*\*)						# Power operator
      | (\^|\+|\-|\*|\/|=|\(|\))	# Operators and parentheses
      | (\d+\.\d+|\d+)				# Numbers
      | (i)							# Imaginary unit
      | ([a-zA-Z_]\w*)				# Variables and function names
	  | (\?)						# ? mark
    '''
    tokens = re.findall(token_pattern, expr, re.VERBOSE)
    return [t for group in tokens for t in group if t]

def is_number(token):
    return re.match(r'^\d+(\.\d+)?$', token)

def parse_tokens(tokens):
    output = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Handle unary minus before a number: -5 → '-5'
        if (
            token == '-' and
            i + 1 < len(tokens) and is_number(tokens[i + 1]) and
            (i == 0 or tokens[i - 1] in ('(', '+', '-', '*', '/', '^', '='))
        ):
            output.append('-' + tokens[i + 1])
            i += 2
            continue
        
        # Function call: f(x)
        if token.isalpha() and i + 1 < len(tokens) and tokens[i + 1] == '(':
            func_name = token
            depth = 1
            i += 2
            group = []
            while i < len(tokens):
                if tokens[i] == '(':
                    depth += 1
                elif tokens[i] == ')':
                    depth -= 1
                    if depth == 0:
                        break
                group.append(tokens[i])
                i += 1
            output.append(('FUNC', func_name, parse_tokens(group)))

        else:
            output.append(token)

        i += 1

    return output

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

def parse_num(token):
	if isinstance(token, Node) or isinstance(token, Complex) or isinstance(token, Rational):
		return token
	if token == 'i':
		return Complex(0, 1)
	if token.isalpha():
		return token #Variable(token, None)
	if '.' in token:
		return Rational(float(token))
	else:
		return Rational(int(token))
    
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

        return parse_num(token), index + 1

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
