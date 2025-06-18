# contains get_function_value

from variable import Variable
from polynomial import Polynomial, RationalExpression, plug_in_var
from complex import Complex
from rational import Rational
from tools import get_value
from node import Node

# !!!! big modifications for modulo
def get_function_value(func_name, func_var, history):
    """get the value of a function at a certain point"""
    function = get_value(func_name, history)

    history_copy = history
    history_copy[function.var] = func_var

    # print("in get function value", function)

    if function is None:
        print("Error: function is not defined")
        return None

    # check for variable
    variable = func_var
    if variable == 'i':
        variable = Complex(0, 1)
    if isinstance(variable, str):
        if variable.isalpha():
            variable = Variable(variable, None)
        elif '.' in variable:
            variable = Rational(float(variable))
        else:
            variable = Rational(int(variable))
    if isinstance(variable, Node):
        if variable.type == 'VAR':
            variable = variable.left

    print("1234", variable, function, type(function))

    if isinstance(variable, str):
        sol = function.terms.solve_node(history_copy)
        return sol
    elif isinstance(function, (Polynomial, RationalExpression)):
        print("before plug vars")
        function = function.plug_vars(history_copy)
        print("after plug vars", function, function.var)
        # check for division by zero
        if isinstance(function, RationalExpression):
            dem = function.denominator
            ex = 0
            while isinstance(dem, Polynomial) and ex == 0:
                if dem.get_degree() == 0:
                    dem = dem.get_coefficients(0)[0]
                    if dem == 0:
                        print("division by zero")
                        return None
                    elif not isinstance(dem, Polynomial):
                        ex = 1
                else:
                    ex = 1
        print("before plug in var", function, variable)
        sol = plug_in_var(function, variable, history_copy)
        print("after plug in var", variable, sol, type(sol), sol.var)
        if isinstance(sol, Polynomial):
            if sol.get_degree() == 0:
                sol = sol.get_coefficients(0)[0]
        return sol
    elif isinstance(function, Node):
        if isinstance(function.left, (Polynomial, RationalExpression)):
            function.left = function.left.plug_vars(history_copy)
            sol_left = plug_in_var(function.left, variable, history_copy)
            if isinstance(sol_left, Polynomial):
                if sol_left.get_degree() == 0:
                    sol_left = sol_left.get_coefficients(0)[0]
        else:
            print("not a poly left")
            return None
        if isinstance(function.right, (Polynomial, RationalExpression)):
            function.right = function.right.plug_vars(history_copy)
            sol_right = plug_in_var(function.right, variable, history_copy)
            if isinstance(sol_right, Polynomial):
                if sol_right.get_degree() == 0:
                    sol_right = sol_right.get_coefficients(0)[0]
        else:
            print("not a poly right")
            return None
        sol = sol_left % sol_right
        return sol
    else:
        print("function not poly/rational or otherwise", function, type(function))
    return None
