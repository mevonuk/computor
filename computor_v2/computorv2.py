from complex import Complex
from parse import parse_cmd


def print_instructions():
    """Prints out instructions for user at start of program"""
    print("Welcome to computor_v2 by mevonuk")
    print("This calculator supports rational and complex numbers,")
    print("matrices, vectors, and simple functions.")
    print("\nAcceptible input:")
    print("\tvariable = value")
    print("\tmatrix = [[v1,v2];[v3,v4]]")
    print("\tfunction(var) = expression")
    print("\tExpression = ? (to return value of expression)")
    print("\tfunction(var) = expression ? (to solve for var)\n")
    print("To exit the program, enter 'exit'\n")


def main():
    """main control for computor_v2, a code to serve as
    a simple calculator for functions and matrices"""
    # print_instructions()

    cmd = ""
    history = {}

    history['i'] = Complex(0, 1)

    while (1):
        try:
            cmd = input("> ")
            if cmd == 'exit':
                exit()

            if cmd:
                key, value = parse_cmd(cmd, history)
                if key and value:
                    history[key] = value

        except (TypeError, Exception, KeyboardInterrupt) as e:
            if isinstance(e, KeyboardInterrupt):
                print("\nInterrupted! Exiting program.")
                exit()
            else:
                print(e)


if __name__ == "__main__":
    main()
