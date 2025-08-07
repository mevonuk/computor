# contains: check_equal_signs, check_decimals, check_new_term,
# insert_mult, check_input_chars, count_paren, check_user_input

import re


def check_user_input(s: str) -> int:
    """checks the users input for characters, peren, etc."""
    if not isinstance(s, str):
        raise TypeError("Error: Bad input to parcer, not a string")

    if check_input_chars(s) == 1:
        return 1
    if check_equal_signs(s) == 1:
        return 1
    if check_decimals(s) == 1:
        return 1
    if check_new_term(s) == 1:
        return 1
    if count_paren(s) == 1:
        return 1
    if check_i(s) == 1:
        return 1
    if check_matrix(s) == 1:
        return 1
    return 0


def check_matrix(s: str) -> int:
    """check if trying to do crazy stuff with a matrix"""
    # rm excess spaces
    s2 = s.replace(" ", "")
    s_list = list(s2)
    for i, c in enumerate(s_list):
        if c == '[':
            if i > 0:
                if s_list[i-1] in set('%/^'):
                    print("Error: undefined matrix/vector operation")
                    return 1
        if c == ']':
            if i + 1 < len(s_list):
                if s_list[i+1] in set('%'):
                    print("Error: undefined matrix/vector operation")
                    return 1
        if c == ';':
            if i + 1 < len(s_list):
                if s_list[i+1] != '[':
                    print("Error: bad format")
                    return 1
            if i > 0:
                if s_list[i-1] != ']':
                    print("Error: bad format")
                    return 1
    return 0


def check_i(s: str) -> int:
    """checks if i is followed by a digit"""
    s_list = list(s)
    for i, c in enumerate(s_list):
        if c == 'i':
            if i + 1 < len(s_list):
                if s_list[i+1].isdigit():
                    print("Error: bad format")
                    return 1
    return 0


def check_equal_signs(s: str):
    """checks the number of equal signs in the input"""
    count = s.count('=')
    if count != 1:
        print("Error: Equation should have 1 equal sign.")
        return 1
    if s.index('=') == 0:
        print("Error: leading =")
        return 1
    return 0


def check_decimals(s: str):
    """checks the number of decimals in a single term"""
    s_list = list(s)
    for i, c in enumerate(s_list):
        if c == '.':
            if i + 1 < len(s_list):
                sub_list = s_list[i + 1:]
                for cc in sub_list:
                    if cc == '.' or cc.isalpha():
                        print("Error: Bad input, check decimal points.")
                        return 1
                    if not cc.isdigit():
                        break
    return 0


def check_new_term(s: str):
    """Checks to see if a new term starts after certain characters"""
    s_list = list(s)
    c_new_term = set('+-=(*/%^i')
    for i, c in enumerate(s_list):
        if c.isdigit() or c == '.' or c.isalpha() or c == ')':
            if i + 1 < len(s_list) and s_list[i + 1] == ' ':
                if i + 2 < len(s_list):
                    sub_list = s_list[i + 2:]
                    for cc in sub_list:

                        if cc in c_new_term:
                            break
                        if cc.isdigit() or cc.isalpha():
                            print("Error: Poorly written term")
                            return 1
    return 0


def insert_mult(s: str) -> str:
    """Inserts a multiplication sign between certain characters"""
    s = re.sub(r'(?<=[0-9a-zA-Z\)])\s+(?=[a-zA-Z\(])', ' * ', s)
    return s


def check_input_chars(s: str):
    """Checks allowed characters"""
    CHAR_ALLOWED = set('+-/*^% ()=?.;[],')
    for c in s:
        if not c.isalpha() and not c.isdigit() and c not in CHAR_ALLOWED:
            print("Error: Not an allowed char:", c)
            return 1
    return 0


def count_paren(s):
    """Counts the number of parentheses and brakets to check for balance"""
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
