import re


def check_term(coef_str: str, exp_str: str, match: str):
    """check each term to make sure both
    the coef and the exp are valid"""
    if not isinstance(coef_str, str):
        raise TypeError("for check_term, coef must be str")
    if exp_str is not None:
        if not isinstance(exp_str, str):
            raise TypeError("for check_term, exp must be str")
    if not isinstance(match, str):
        raise TypeError("for check_term, match must be str")

    # Validate coefficient
    if not coef_str[0] in ("+", "-"):
        raise Exception('Error: Invalid entry.')

    # Validate exponent
    if exp_str is not None:
        if not exp_str.isdigit():
            raise Exception("Error: Invalid exponent.")


def parse_side(expr: str) -> dict:
    """parse side of equation, expr, by term into a dictionary
    using the exp as the key using the term_pat to recognise
    the terms"""
    if not isinstance(expr, str):
        raise TypeError("for parse_side, expr must be str")

    # Pattern to extract terms: coeff group (optional exponent group)
    term_pat = r'([+-]?(?:\d+(?:\.\d*)?|\.\d+)?)(?:\*?x(?:\^([^\s+*-]+))?)?'
    # coeff group: ([+-]?(?:\d+(?:\.\d*)?|\.\d+)?)
    #     [+-]? optional sign
    #     (?:\d+(?:\.\d*)?|\.\d+)?) int or float
    #           ?:... non-capturing, group formed for logic, not saved
    #           ...? optional
    #           \d+ one or more digits (int part)
    #           \. decimal point
    #           \d* zero or mor digits
    # optional exponent group: (?:\*?x(?:\^([^\s+*-]+))?)?
    #     ?:\*? optional *
    #     x required
    #     (?:\^([^\s+*-]+))?) optional exponent
    #           \^ literal carot
    #           ([^\s+*-]+) excludes spaces, +, *, -

    db = {}
    for match in re.finditer(term_pat, expr):
        coef_str, exp_str = match.groups()

        # Skip empty matches
        if not coef_str and not exp_str:
            continue

        try:
            check_term(coef_str, exp_str, match.group())
        except (TypeError, Exception) as e:
            print(e)
            exit()

        # convert coefficient to float
        if coef_str in ("+", "-"):
            coef = float(coef_str + "1")
        else:
            coef = float(coef_str) if coef_str else 1.0

        # convert exponent to int
        if exp_str is not None:
            exp = int(exp_str)
        else:
            exp = 1 if 'x' in expr[match.start():match.end()] else 0

        # assign coef to key (add to existing if necessary)
        db[exp] = db.get(exp, 0) + coef
    return db


def ensure_sign(s: str) -> str:
    """Ensure that each equation expresion starts with + or -"""
    if not isinstance(s, str):
        raise TypeError("for ensure_sign, s must be str")
    if s and s[0] not in ('+', '-'):
        return '+' + s
    return s


def parse_polynomial(equation: str) -> dict:
    """parse equation to a dictionary with key = exp
    and value = coef"""
    if not isinstance(equation, str):
        raise TypeError("for parse_polynomial, equation must be str")

    # Split left and right side of the equation
    left, right = equation.replace(" ", "").split("=")

    if not left or not right:
        raise Exception("Error: Equation is not complete.")

    # add + sign at beginning if necessary
    left = ensure_sign(left)
    right = ensure_sign(right)

    # parse the two sides of the equation
    try:
        db_l = parse_side(left)
        db_r = parse_side(right)
    except (TypeError, Exception) as e:
        print(e)
        exit()

    # Combine db_l and db_r into a new dictionary db_total
    db_total = db_l.copy()  # Start with left-hand side terms

    # subtract right-hand terms
    for exp, coef in db_r.items():
        db_total[exp] = db_total.get(exp, 0) - coef

    if not db_total:
        raise Exception("Error: Empty polynomial.")

    # determine the min and max degrees of the polynomial
    max_exp = max(db_total.keys())
    print("Input polynomial degree:", max_exp)
    min_exp = min(db_total.keys())

    # Collect keys to remove
    keys_to_remove = [exp for exp, coef in db_total.items() if coef == 0]

    # Remove keys after iteration
    for key in keys_to_remove:
        db_total.pop(key)

    if min_exp > 0 and min_exp == max_exp and not db_total:
        print("\nPossible solutions include: x = 0")

    if db_total:
        min_exp = min(db_total.keys())
        if min_exp > 0:
            print("\nPossible solutions include: x = 0")

        # Shift exponents so that the lowest becomes 0
        while (min_exp := min(db_total.keys())) > 0:
            db_total = {exp - min_exp: coef for exp, coef in db_total.items()}

            # Collect keys to remove
            to_remove = [exp for exp, coef in db_total.items() if coef == 0]

            # Remove keys after iteration
            for key in to_remove:
                db_total.pop(key)

    return db_total
