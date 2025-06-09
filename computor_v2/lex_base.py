# contains: tokenize, is_number, parse_tokens, parse_matrix_literal,
# extract_matrix_literal, split_terms, parse_number, parse_num_raw

import re
from matrix import Matrix, Vector
from rational import Rational
from complex import Complex


def tokenize(expr):
    """Tokenize expression"""
    # Only insert * where it's clearly implied,
    # not between a function name and (
    # Insert * between number and variable or (
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    # Insert * between ) and variable or number
    expr = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', expr)
    # Insert * between variable and another variable (e.g., x y → x*y)
    expr = re.sub(r'([a-zA-Z])\s+([a-zA-Z])', r'\1*\2', expr)
    # DO NOT insert * between variable and ( — that breaks function calls

    # Replace unary minus before variables (e.g., -x -> -1*x),
    # but NOT before numbers
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
    """Check if token is an int or float"""
    return re.match(r'^\d+(\.\d+)?$', token)


def parse_tokens(tokens):
    """Parse tokens detecting functions"""
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


def extract_matrix_literal(s):
    """Parse tokens for matrix/vector"""
    pattern = r'\[\[.*?\]\]'  # non-greedy match for matrix
    matches = re.findall(pattern, s)
    matrix_type = 2  # matrix type
    if not matches:
        pattern = r'\[.*?\]'  # non-greedy match for matrix
        matches = re.findall(pattern, s)
        matrix_type = 1  # vector type
    if not matches:
        matrix_type = 0  # not a matrix or vector type
    return matches, matrix_type


def split_terms(s):
    """Split terms based on addition/subtraction"""
    return re.findall(r'[+-]?\s*[^+-]+', s)


def parse_number(token):
    """Parse number tokens into Complex or Rational"""
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
    """Parse matrix tokens"""
    # Remove outer brackets
    rows = matrix_str.split(';')
    # remove brackets
    num_col = -1
    matrix_data = []
    for row in rows:
        row = row.replace('[', '')
        row = row.replace(']', '')
        new_row = []
        for term in row.split(','):
            term = term.strip()
            # parse term here
            term = parse_number(term)
            new_row.append(term)
        num_col_old = num_col
        num_col = len(new_row)
        if num_col_old != -1 and num_col_old != num_col:
            print("Error: All cols of a matrix should have the same length")
            return None
        matrix_data.append(new_row)
    if matrix_type == 2:
        return Matrix(matrix_data)
    else:
        return Vector(matrix_data)


def parse_num_raw(token):
    """Parse token into Complex, Rational, or string"""
    # print("in parse_num_raw", token, type(token))
    if token == 'i':
        return Complex(0, 1)
    if token.isalpha():
        return token
    if '.' in token:
        return Rational(float(token))
    else:
        return Rational(int(token))

