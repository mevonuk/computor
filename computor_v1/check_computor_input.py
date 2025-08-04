# check the user input to see if it conforms to the
# program specifications,
# modify string to standardize,
# and perform final checks
# contains: check_chars, check_equals, check_multple_decimals,
# check_spaces, check_input_chars, modify_exp,
# check_exp, check_sign, check_decimals, check_mult, check_input

def check_chars(s: str):
    """check for allowed characters"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")
    CHAR_ALLOWED = set('0123456789.+-=* ^xX')
    for c in s:
        if c not in CHAR_ALLOWED:
            raise Exception(f"Error: Not an allowed char: {c}")


def check_equals(s: str):
    """checks the number of equal signs"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")
    count = s.count('=')
    if count != 1:
        raise Exception("Error: Equation should have 1 equal sign.")


def check_multple_decimals(s: str):
    """checks for multiple decimal points in the same term"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")
    s_list = list(s)
    for i, c in enumerate(s_list):
        if c == '.':
            if i + 1 < len(s_list):
                sub_list = s_list[i + 1:]
                for cc in sub_list:
                    if cc == '.':
                        raise Exception(
                            "Error: Bad input, check decimal points."
                            )
                    if cc in ("+", "-", "x", "X", "="):
                        break


def check_spaces(s: str):
    """check spaces to see if a new term starts"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")
    s_list = list(s)
    for i, c in enumerate(s_list):
        if c.isdigit() or c == '.':
            if i + 1 < len(s_list) and s_list[i + 1] == ' ':
                if i + 2 < len(s_list):
                    sub_list = s_list[i + 2:]
                    for cc in sub_list:
                        if cc in ("+", "-", "x", "X", "="):
                            break
                        if cc.isdigit():
                            raise Exception("Error: Poorly written coef.")


def check_input_chars(s: str):
    """Checks that only allowed characters are used,
    checks the number of = signs,
    checks for multiple . in a single term
    and checks that new terms start properly"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")

    try:
        check_chars(s)
        check_equals(s)
        check_multple_decimals(s)
        check_spaces(s)
    except (TypeError, Exception) as e:
        print(e)
        return None


def modify_exp(s: str):
    """if x is not followed by ^ insert this"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")
    s_list = list(s)
    for i, c in enumerate(s_list):
        if c == 'x':
            # Check if the next character is not '^'
            if i + 1 < len(s_list):
                if s_list[i + 1] != '^':
                    # insert '^' if missing before number
                    if s_list[i + 1].isdigit():
                        s_list.insert(i + 1, '^')
                    # Insert "^1" after 'x' (if not already followed by '^')
                    else:
                        s_list.insert(i + 1, '^')
                        s_list.insert(i + 2, '1')
            else:
                # Insert "^1" after 'x' if at end of string
                s_list.insert(i + 1, '^')
                s_list.insert(i + 2, '1')
    # Convert the list back to a string
    modified_s = ''.join(s_list)
    return modified_s


def check_exp(s: str):
    """checks that exponents are ints"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")
    s_list = list(s)
    for i, c in enumerate(s_list):
        if c == '^':
            # check that next char is digit
            if i + 1 < len(s_list):
                if not s_list[i + 1].isdigit():
                    raise Exception("Error: Bad exponent")
            else:
                raise Exception("Error: Empty exponent")


def check_sign(s: str):
    """checks that + and - are followed by digit, ., or x"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")
    s_list = list(s)
    for i, c in enumerate(s_list):
        if c == '+' or c == '-':
            # check that next char is digit, '.', or 'x'
            if i + 1 < len(s_list):
                if not s_list[i + 1].isdigit():
                    if s_list[i + 1] not in {'.', 'x'}:
                        raise Exception("Error: Bad input")
            else:
                raise Exception("Error: trailing sign")


def check_decimals(s: str):
    """check '.' to see if there is a number to either side"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")
    s_list = list(s)
    for i, c in enumerate(s_list):
        if c == '.':
            if s_list[i - 1].isdigit():
                continue
            if i + 1 < len(s_list):
                if s_list[i + 1].isdigit():
                    continue
                else:
                    raise Exception("Error: Bad input, check decimal points")
            else:
                raise Exception("Error: Bad input, check decimal points")


def check_mult(s: str):
    """Check that multiplication sign is used properly"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")
    s_list = list(s)
    for i, c in enumerate(s_list):
        if c == '*':
            if s_list[i - 1] == '=':
                raise Exception("Error: Invalid use of '*'")
            if i + 1 < len(s_list):
                sub_list = s_list[i + 1:]
                for cc in sub_list:
                    if cc not in (" ", "x", "X"):
                        raise Exception("Error: Invalid use of '*'")
                    if cc in ("x", "X"):
                        break
            else:
                raise Exception("Error: Invalid use of '*'")


# check input characters, remove spaces, make all Xs lowercase, set x -> x^1
def check_input(s):
    """Checks input characters,
    removes spaces,
    makes everything lowercase,
    sets x to x^1"""
    if not isinstance(s, str):
        raise TypeError("Input not a string")

    # check the input characters for various problems
    check_input_chars(s)

    # modify string:
    # remove all spaces
    s = s.replace(" ", "")
    # change X to x
    s = s.replace("X", "x")
    # standardize exponentials
    s = modify_exp(s)

    # perform checks on modified string
    try:
        check_exp(s)
        check_sign(s)
        check_decimals(s)
        check_mult(s)
    except (TypeError, Exception) as e:
        print(e)
        return None

    return s
