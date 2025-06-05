import sys
from my_math_tools import sqrt, abs, reduce
from check_computor_input import check_input
from parse_computor import parse_polynomial


def print_polynomial(db: dict):
    """Convert polynomial to string for printing"""
    if not isinstance(db, dict):
        raise TypeError("for print_polynomial, input must be dict")
    terms = []

    # Sort terms by exponent ascending
    for exp in sorted(db, reverse=False):
        coef = db[exp]
        if coef == 0:
            continue

        # Format coefficient
        sign = '+' if coef > 0 else '-'
        abs_coef = int(abs(coef)) if abs(coef).is_integer() else abs(coef)

        # Format term
        if exp == 0:
            term = f"{abs_coef}"
        elif exp == 1:
            if abs_coef == 1:
                term = "x"
            else:
                term = f"{abs_coef}x"
        else:
            if abs_coef == 1:
                term = f"x^{exp}"
            else:
                term = f"{abs_coef}x^{exp}"

        terms.append(f" {sign} {term}")

    if not terms:
        return "0 = 0"

    # First term: remove leading '+' and space
    result = terms[0].lstrip(" +")
    # Add the rest
    result += ''.join(terms[1:])

    return result + " = 0"


def main():
    """main control for computor, a code to simplify and
    solve simple polynomial equations (quadratic and lower)"""

    try:
        if len(sys.argv) != 2:
            print("Wrong number of arguments")
            return

        # check input and remove spaces `and other error checks
        equation = check_input(sys.argv[1])

        result = parse_polynomial(equation)

        print("\nReduced form:", print_polynomial(result), "\n")

        if not result:
            print("Any real number is a solution;")
            print("x does not appear in the reduced equation.")
            return

        # check largest exponent
        max_exp = max(result.keys())

        print("Reduced Polynomial degree:", max_exp)

        if max_exp > 2:
            print("The reduced polynomial degree is strictly greater than 2,")
            print("there is no simple solution.\n")
            return

        # solve reduced equation
        if max_exp == 0:
            print("No solution for (reduced) equation.")

        if max_exp == 1:
            print("Solving (reduced) linear equation...")
            a = int(result[0]) if result[0].is_integer() else result[0]
            b = int(result[1]) if result[1].is_integer() else result[1]
            print("\nSolution:", reduce(-a, b, 0))

        if max_exp == 2:
            print("Solving quadratic equation...")
            a = int(result[2]) if result[2].is_integer() else result[2]
            c = int(result[0]) if result[0].is_integer() else result[0]
            if 1 in result:
                b = int(result[1]) if result[1].is_integer() else result[1]
            else:
                b = 0
            discriminant = b * b - 4 * a * c
            if discriminant > 0:
                print("\nDiscriminant is positive: two real solutions:")
                top = -b + sqrt(discriminant)
                top = int(top) if top.is_integer() else top
                print(reduce(top, 2 * a, 0))
                top = -b - sqrt(discriminant)
                top = int(top) if top.is_integer() else top
                print(reduce(top, 2 * a, 0))
            elif discriminant == 0:
                print("\nDiscriminant is zero: one real solution:")
                print(f"{reduce(-b, 2 * a, 0)}")
            else:
                print("\nDiscriminant is negative: two complex solutions:")
                reduced_realterm = reduce(-b, 2 * a, 0)
                sqrtd = sqrt(abs(discriminant))
                sd = int(sqrtd) if sqrtd.is_integer() else sqrtd
                reduced_imagterm = reduce(sd, 2 * a, 1)
                if reduced_imagterm and reduced_imagterm[0] == '-':
                    reduced_imagterm = reduced_imagterm[1:]
                print(f"{reduced_realterm} + {reduced_imagterm}")
                print(f"{reduced_realterm} - {reduced_imagterm}")
        print("")

    except (TypeError, Exception) as e:
        print(e)


if __name__ == "__main__":
    main()
