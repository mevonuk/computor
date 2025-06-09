# contains get_function_value

from variable import Variable
from polynomial import Polynomial, RationalExpression, plug_in_var
from complex import Complex
from rational import Rational
from tools import get_value


def get_function_value(func_name, func_var, history):
    """get the value of a function at a certain point"""
    function = get_value(func_name, history)

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

    if isinstance(variable, str):
        sol = function.terms.solve_node(history)
        return sol
    elif isinstance(function, (Polynomial, RationalExpression)):
        function = function.plug_vars(variable, history)
        sol = plug_in_var(function, variable, history)
        if isinstance(sol, Polynomial):
            if sol.get_degree() == 0:
                sol = sol.get_coefficients(0)[0]
        return sol
    else:
        print("function not poly/rational or otherwise")
    return None
