import re
from matrix import Matrix, Vector
from rational import Rational
from complex import Complex
from function import Term, Polynomial

def tokenize2(expr):
    import re

    # Insert * between number and variable or (
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    # Insert * between ) and variable or number
    expr = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', expr)
    # Insert * between variable and another variable if space between
    expr = re.sub(r'([a-zA-Z])\s+([a-zA-Z])', r'\1*\2', expr)

    token_pattern = r'''
        (\*\*)                        # Power operator
      | (\^|\+|\-|\*|\/|=|\(|\)|\[|\]|,|;)  # Operators, parentheses, brackets, separators
      | (\d+\.\d+|\d+)                # Numbers
      | (i)                           # Imaginary unit
      | ([a-zA-Z_]\w*)                # Variables or function names
    '''
    tokens = re.findall(token_pattern, expr, re.VERBOSE)
    return [t for group in tokens for t in group if t]

def tokenize(expr):
    # Only insert * where it's clearly implied, not between a function name and (
    # Insert * between number and variable or (
    expr = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', expr)
    # Insert * between ) and variable or number
    expr = re.sub(r'(\))([a-zA-Z0-9])', r'\1*\2', expr)
    # Insert * between variable and another variable (e.g., x y → x*y)
    expr = re.sub(r'([a-zA-Z])\s+([a-zA-Z])', r'\1*\2', expr)
    # DO NOT insert * between variable and ( — that breaks function calls

    token_pattern = r'''
        (\*\*)                    # Power operator
      | (\^|\+|\-|\*|\/|=|\(|\))   # Operators and parentheses
      | (\d+\.\d+|\d+)            # Numbers
      | (i)                       # Imaginary unit
      | ([a-zA-Z_]\w*)            # Variables and function names
    '''
    tokens = re.findall(token_pattern, expr, re.VERBOSE)
    return [t for group in tokens for t in group if t]

def parse_tokens(tokens):
    output = []
    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Multiplication with group: f * (x)
        if token == '*' and i + 1 < len(tokens) and tokens[i + 1] == '(':
            i += 2
            depth = 1
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
            output.append('*')
            output.append(('PAREN', parse_tokens(group)))
        
        # Function call: f(x)
        elif token.isalpha() and i + 1 < len(tokens) and tokens[i + 1] == '(':
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

        # Grouped expression by itself: (x + 1)
        elif token == '(':
            i += 1
            depth = 1
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
            output.append(('PAREN', parse_tokens(group)))

        else:
            output.append(token)

        i += 1

    return output

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

def parse_term(s):
    import re
    s = s.replace(' ', '')
    s_list = list(s)

    # Fix implicit multiplications
    i = 0
    while i < len(s_list) - 1:
        if s_list[i] == ')' and s_list[i+1] not in '+-*/^)':
            s_list.insert(i+1, '*')
        elif s_list[i].isdigit() and s_list[i+1] == '(':
            s_list.insert(i+1, '*')
        elif s_list[i].isdigit() and s_list[i+1].isalpha():
            s_list.insert(i+1, '*')
        elif s_list[i].isalpha() and s_list[i+1] == '(':
            s_list.insert(i+1, '*')
        elif s_list[i] == '-' and s_list[i+1].isalpha():
            s_list.insert(i+1, '1*')
        i += 1

    s = ''.join(s_list)
    print("Adjusted string:", s)

    #term_pattern = r'([*/]?)' + r'([+-]?(?:\([^()]+\)|[a-zA-Z0-9_.+-]+))' + r'(?:\*?([a-zA-Z_][a-zA-Z_0-9]*)(?:\^(-?\d+))?)?'
    term_pattern = r'([*/]?)' + r'([+-]?(?:\([^()]+\)|\d+(?:\.\d*)?|\.\d+)?)(?:\*?([a-zA-Z_][a-zA-Z_0-9]*)(?:\^(-?\d+))?)?'

    poly_list = []

    for match in re.finditer(term_pattern, s):
        op, coef_str, var_str, exp_str = match.groups()
        if not coef_str and not var_str:
            continue

        coef = 1
        exp = 0
        var = "dummy_var"

        print("Match:", coef_str, var_str, exp_str, op)

        # Handle sub-expressions (e.g., (x+1))
        if coef_str.startswith('(') and coef_str.endswith(')'):
            inner_expr = coef_str[1:-1]
            sub_poly = parse_term(inner_expr)
            print(sub_poly)
            if poly_list:
                if op == '*':
                    p = poly_list[-1]
                    p2 = p  * sub_poly
                    poly_list.pop()
                    poly_list.append(p2)
                elif op == '/':
                    print("Division of polys not yet supported.")
                    exit()
            else:
                poly_list.append(sub_poly)
            continue

        # Handle plain terms or variables
        if var_str:
            var = var_str
            exp = 1
        if exp_str:
            exp = int(exp_str)

        if not var_str and coef_str.isalpha():  # Pure variable, like 'x'
            coef = 1
            var = coef_str
            exp = 1
        elif coef_str:
            coef = parse_number(coef_str)


        term = Term(coef, var, exp, '+')
        print("term", term)

        if poly_list and op == '*':
            p = poly_list[-1]
            p2 = Polynomial()
            p2.add_term(term)
            poly_list.pop()
            poly_list.append(p * p2)
        else:
            p = Polynomial()
            p.add_term(term)
            print(p)
            poly_list.append(p)

        print("poly_list", poly_list)

    poly = Polynomial()
    for p in poly_list:
        poly = poly + p

    return poly


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
