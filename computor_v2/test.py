from complex import Complex
from parse import parse_cmd
from variable import Variable


def print_instructions():
	print("Welcome to computor_v2 by mevonuk")
	print("This calculator supports rational and complex numbers,")
	print("matrices, vectors, and simple functions.")
	print("\nAcceptible input:")
	print("\tvariable_name = expression (to assign a value to a variable)")
	print("\tExpression = ? (to solve expression)\n")
	print("To exit the program, enter 'exit'\n")


# print_instructions()

# tests:
# assigning matrix
# solving matrix containing functions and variables
# assigning functions
# solving functions, with variables and plugging in value of 'x' in ()
# assigining variables, setting equal to other variables
# solving with variables, functions
# solving quadratic equations

# need to be able to determine how many undefined variables there are
# then if 1, check the power, then if 2 or smaller, solve for the variable


history = {}

s = "f(y) = 4*2%y"
print('>', s)
key, value = parse_cmd(s, history)
if key is not None and value is not None:
	history[key] = value

s = "f(3) = ?"
print('>', s)
key, value = parse_cmd(s, history)
if key is not None and value is not None:
	history[key] = value

exit()

cmd = ""
history = {}

history['i'] = Complex(0, 1)

while(1):
	cmd = input("> ")
	if cmd == 'exit':
		exit()

	if cmd:
		# print(cmd)
		key, value = parse_cmd(cmd, history)
		if key and value:
			history[key] = value

	# print(history)