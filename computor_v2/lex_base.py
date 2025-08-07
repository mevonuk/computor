# contains: tokenize, is_number, parse_tokens,
# extract_matrix_literals, split_terms, parse_number, parse_num_raw, parse_num

import re

from rational import Rational
from complex import Complex
from variable import Variable
from node import Node


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


def parse_num(token):
    """Takens token and converts it if necessary"""
    if isinstance(token, tuple):
        return None
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

def extract_matrix_literals(expr):
    """Extract matrix and vector literals and replace them with placeholders"""
    matrix_vector_pattern = r'\[(?:\[.*?\]|[^\[\]])*?\]'

    matches = []
    placeholders = []
    typed_literals = {}
    i = 0

    def classify_literal(literal):
        if literal.startswith('[[') and literal.endswith(']]'):
            return 'MATRIX'
        elif ';' in literal:
            return 'MATRIX'
        else:
            return 'VECTOR'

    def replacer(match):
        nonlocal i
        literal = match.group()
        literal_type = classify_literal(literal)
        placeholder = f"__MATRIX{i}__"
        matches.append(literal)
        placeholders.append(placeholder)
        typed_literals[placeholder] = (literal_type, literal)
        i += 1
        return placeholder

    # Use finditer to do safe non-overlapping replacement
    new_expr = ""
    last_end = 0
    for m in re.finditer(matrix_vector_pattern, expr):
        new_expr += expr[last_end:m.start()]
        new_expr += replacer(m)
        last_end = m.end()
    new_expr += expr[last_end:]

    return new_expr, typed_literals


def tokenize(expr):
    """Tokenize expression with matrix/vector support"""
    expr, literal_map = extract_matrix_literals(expr)

    # Insert implicit multiplications
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    expr = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', expr)
    expr = re.sub(r'([a-zA-Z])\s+([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(?<![\w\)])-(?=[a-zA-Z_])', r'-1*', expr)

    token_pattern = r'''
        (\*\*)                           # Power operator
      | (\^|\+|\-|\*|\/|=|\(|\)|\%)      # Operators and parentheses
      | (\d+\.\d+|\d+)                  # Numbers
      | (__MATRIX\d+__)                # Matrix/vector placeholders
      | ([a-zA-Z_]\w*)                 # Variables and function names
      | (\?)                            # ? mark
    '''

    tokens = re.findall(token_pattern, expr, re.VERBOSE)
    flat_tokens = [t for group in tokens for t in group if t]

    # Replace placeholders with tagged literals
    final_tokens = [
        literal_map[t] if t in literal_map else t
        for t in flat_tokens
    ]

    return final_tokens


def is_number(token):
    return isinstance(token, str) and re.match(r'^\d+(\.\d+)?$', token)


def parse_tokens(tokens):
    """Parse tokens detecting functions and unary minus"""
    output = []
    SPECIAL_TOKENS = ('(', '+', '-', '*', '/', '%', '^', '=')
    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Tagged matrix/vector literals → pass through
        if isinstance(token, tuple) and token[0] in ('MATRIX', 'VECTOR'):
            output.append(token)
            i += 1
            continue

        if (
            token == '-' and
            i + 1 < len(tokens) and is_number(tokens[i + 1]) and
            (i == 0 or tokens[i - 1] in SPECIAL_TOKENS)
        ):
            output.append('-' + tokens[i + 1])
            i += 2
            continue

        # Function call detection: f(x)
        if isinstance(token, str) and token.isalpha() and i + 1 < len(tokens) and tokens[i + 1] == '(':
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
