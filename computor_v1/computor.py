import sys	# for input and exit
import re	# for character matching redex
from my_math_tools import sqrt, abs
	
# check user input
def check_input_chars(s):
	if not isinstance(s, str):
		print("Error: Not a string")
		sys.exit()

	# check for allowed characters
	chars = set('0123456789.+-=* ^xX')
	for c in s:
		if c not in chars:
			print("Error: Not an allowed char:", c)
			sys.exit()
	# check number of = signs
	count = s.count('=')
	if count != 1:
		print("Error: Equation should have 1 equal sign.")
		sys.exit()

	# check multiple . in one term
	s_list = list(s)
	for i, c in enumerate(s_list):
		if c == '.':
			if i + 1 < len(s_list):
				sub_list = s_list[i + 1:]
				for cc in sub_list:
					if cc == '.':
						print("Error: Bad input, check decimal points.")
						sys.exit()
					if cc in ("+", "-", "x", "X", "="):
						break

	# check spaces to see if a new term starts
	s_list = list(s)
	for i, c in enumerate(s_list):
		if c.isdigit() or c == '.':
			if i + 1 < len(s_list) and  s_list[i + 1] == ' ':
				if i + 2 < len(s_list):
					sub_list = s_list[i + 2:]
					for cc in sub_list:
						if cc in ("+", "-", "x", "X", "="):
							break
						if cc.isdigit():
							print("Error: Poorly written coef.")
							sys.exit()


# check input characters, remove spaces, make all Xs lowercase, set x -> x^1
def check_input(s):
	if not isinstance(s, str):
		print("Error: not a string")
		sys.exit()

	# check that only allowed characters are entered
	check_input_chars(s)

	# remove all spaces
	s = s.replace(" ", "")
	# change X to x
	s = s.replace("X", "x")

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

	for i, c in enumerate(s_list):
		if c == '^':
			# check that next char is digit
			if i + 1 < len(s_list):
				if not s_list[i + 1].isdigit():
					print("Error: Bad exponent.")
					sys.exit()
			else:
				print("Error: Bad exponent.")
				sys.exit()
		if c == '+' or c == '-':
			# check that next char is digit, '.', or 'x'
			if i + 1 < len(s_list):
				if not s_list[i + 1].isdigit() and s_list[i + 1] not in {'.', 'x'}:
					print("Error: Bad input")
					sys.exit()

	# Convert the list back to a string
	modified_s = ''.join(s_list)

	# check '.' to see if there is a number to either side
	s_list = list(modified_s)
	for i, c in enumerate(s_list):
		if c == '.':
			if s_list[i - 1].isdigit():
				continue
			if i + 1 < len(s_list):
				if s_list[i + 1].isdigit():
					continue
				else:
					print("Error: Bad input, check decimal points")
					sys.exit()
			else:
				print("Error: Bad input, check decimal points")
				sys.exit()

	# check *
	for i, c in enumerate(s_list):
		if c == '*':
			if s_list[i - 1] == '=':
				print("Error: Invalid use of '*'.")
				sys.exit()
			if i + 1 < len(s_list):
				sub_list = s_list[i + 1:]
				for cc in sub_list:
					if cc not in (" ", "x", "X"):    
						print("Error: Invalid use of '*'.")
						sys.exit()
					if cc in ("x", "X"):    
						break
			else:
				print("Error: Invalid use of '*'.")
				sys.exit()

	return modified_s

def check_term(coef_str, exp_str, match):
	# Validate coefficient
	if not coef_str:
		print("Error: Missing coef:", match)
		sys.exit()

	if not coef_str[0] in ("+", "-"):
		print('Error: Invalid entry.')
		sys.exit()

	# Validate exponent
	if exp_str is not None:
		if not exp_str.isdigit():
			print("Error: Invalid exponent.")
			sys.exit()

# parse string into database
def parse_side(expr, term_pattern):
	db = {}
	for match in re.finditer(term_pattern, expr):
		coef_str, exp_str = match.groups()

		# Skip empty matches
		if not coef_str and not exp_str:
			continue

		check_term(coef_str, exp_str, match.group())

		if coef_str in ("+", "-"):
			coef = float(coef_str + "1")
		else:
			coef = float(coef_str) if coef_str else 1.0

		if exp_str is not None:
			exp = int(exp_str)
		else:
			exp = 1 if 'x' in expr[match.start():match.end()] else 0

		db[exp] = db.get(exp, 0) + coef
	return db

def ensure_sign(s):
	if s and s[0] not in ('+', '-'):
		return '+' + s
	return s

# parse input into a database
def parse_polynomial(equation):
	# Split left and right side of the equation
	left, right = equation.replace(" ", "").split("=")

	if not left or not right:
		print("Error: Equation is not complete.")
		sys.exit()

	# add + sign at beginning if necessary
	left = ensure_sign(left)
	right = ensure_sign(right)

	# Pattern to extract terms: coeff group (optional exponent group)
	term_pattern = r'([+-]?(?:\d+(?:\.\d*)?|\.\d+)?)(?:\*?x(?:\^([^\s+*-]+))?)?'
	# coeff group: ([+-]?(?:\d+(?:\.\d*)?|\.\d+)?)
		# [+-]? optional sign
		# (?:\d+(?:\.\d*)?|\.\d+)?) int or float
			#   ?:... non-capturing, group formed for logic, not saved
			#   ...? optional
			#   \d+ one or more digits (int part)
			#   \. decimal point
			#   \d* zero or mor digits
	# optional exponent group: (?:\*?x(?:\^([^\s+*-]+))?)?
		# ?:\*? optional *
		# x required
		# (?:\^([^\s+*-]+))?) optional exponent
			#   \^ literal carot
			#   ([^\s+*-]+) excludes spaces, +, *, -

	db_l = parse_side(left, term_pattern)
	db_r = parse_side(right, term_pattern)

	# Combine db_l and db_r into a new dictionary db_total
	db_total = db_l.copy()  # Start with left-hand side terms

	# subtract right-hand terms
	for exp, coef in db_r.items():
		db_total[exp] = db_total.get(exp, 0) - coef

	if not db_total:
		print("Error: Empty polynomial.")
		sys.exit()

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
			keys_to_remove = [exp for exp, coef in db_total.items() if coef == 0]

			# Remove keys after iteration
			for key in keys_to_remove:
				db_total.pop(key)

	return db_total

def print_polynomial(db):
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
				term = f"x"
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

# reduce integer faction if possible
def reduce(b, a, type):
	if type not in {0, 1}:
		print("Error: bad usage of reduce()")
		sys.exit()

	if isinstance(b, int) and isinstance(a, int):
		if a * b > 0:
			a = int(abs(a))
			b = int(abs(b))
		factor = 2
		while factor <= min(abs(a), abs(b)):
			while b % factor == 0 and a % factor == 0:
				b = int(b/factor)
				a = int(a/factor)
			factor += 1
		s = f"{b}/{a}"
		if type == 1:
			s = f"{b}i/{a}"
		if abs(b) % abs(a) == 0:
			c = int(b/a)
			s = f"{c}"
			if type == 1:
				s = f"{c}i"
		if abs(b) == abs(a):
			if b * a < 0:
				s = f"-1"
			else:
				s = f"1"
			if type == 1: # don't worry about negative i
				s = f"i"
	else:
		c = b/a
		c = int(c) if c.is_integer() else c
		s = f"{c}"
		if type == 1:
			s = f"{c}i"
	return s


if __name__ == "__main__":
		
	if len(sys.argv) != 2:
		print("Wrong number of arguments")
		sys.exit()

	# check input and remove spaces and other error checks
	equation = check_input(sys.argv[1])

	result = parse_polynomial(equation)

	print("\nReduced form:", print_polynomial(result), "\n")

	if not result:
		print("Any real number is a solution; x does not appear in the reduced equation.")
		sys.exit()

	# check largest exponent
	max_exp = max(result.keys())

	print("Reduced Polynomial degree:", max_exp)

	if max_exp > 2:
		print("The (reduced) polynomial degree is strictly greater than 2, there is no simple solution.\n")
		sys.exit()

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