# contains get_function_value

from variable import Variable
from polynomial import Polynomial, RationalExpression
from complex import Complex
from rational import Rational
from node import Node
from matrix import Matrix

from polynomial import plug_in_var
from tools import get_value
from tree_functions import simplify_node, resolve
from tree_tool import solve_node


def get_function_value(func_name, func_var, history):
    """get the value of a function at a certain point"""
    function = get_value(func_name, history)

    if function is None:
        print("Error: function is not defined")
        return None

    hold_val = get_value(function.var, history)
    hold_key = function.var

    if isinstance(func_var, Variable) and func_var.name == function.var:
        sol = function.solve(history)
        return sol

    if isinstance(func_var, Variable) and func_var.name != function.var:
        func_var = resolve(func_var.name, history)

    history[function.var] = func_var
    
    # check for variable
    variable = func_var
    if variable == 'i':
        variable = Variable(function.var, Complex(0, 1))
    elif isinstance(variable, str):
        if variable.isalpha():
            variable = Variable(variable, None)
        elif '.' in variable:
            variable = Variable(function.var, Rational(float(variable)))
        else:
            variable = Variable(function.var, Rational(int(variable)))
    elif isinstance(variable, Node):
        if variable.type == 'VAR':
            variable = Variable(function.var, variable.left)
    elif isinstance(variable, (int, float, Rational, Complex)):
        variable = Variable(function.var, variable)
    else:
        print("variable type is non-standard")

    if isinstance(variable, Variable) and variable.value is None:
        print('here1')
        if variable.name in history.keys():
            history.pop(variable.name)
        sol = function.solve(history)
        if hold_val is not None:
            history[hold_key] = hold_val
        else:
            history.pop(hold_key)
        return sol
    elif isinstance(function, (Polynomial, RationalExpression)):
        function = function.plug_vars(history)
        # check for division by zero
        if isinstance(function, RationalExpression):
            dem = function.denominator
            ex = 0
            while isinstance(dem, Polynomial) and ex == 0:
                if dem.get_degree() == 0:
                    dem = dem.get_coefficients(0)[0]
                    if dem == 0:
                        print("Error: division by zero")
                        if hold_val is not None:
                            history[hold_key] = hold_val
                        else:
                            history.pop(hold_key)
                        return None
                    elif not isinstance(dem, Polynomial):
                        ex = 1
                else:
                    ex = 1

        sol = plug_in_var(function, variable, history)

        if isinstance(sol, Polynomial):
            if sol.get_degree() == 0:
                sol = sol.get_coefficients(0)[0]
            if isinstance(sol, Node):
                sol = simplify_node(sol, history)

        if isinstance(sol, RationalExpression):
            sol_top = sol.numerator
            sol_bot = sol.denominator
            if sol_top.get_degree() == 0:
                sol_top = sol_top.get_coefficients(0)[0]
            if sol_bot.get_degree() == 0:
                sol_bot = sol_bot.get_coefficients(0)[0]
            if isinstance(sol_top, Node):
                sol_top = simplify_node(sol_top, history)
            if isinstance(sol_bot, Node):
                sol_bot = simplify_node(sol_bot, history)
            if sol_bot == 0:
                print("Error: division by zero")
                if hold_val is not None:
                    history[hold_key] = hold_val
                else:
                    history.pop(hold_key)
                return None
            sol = sol_top / sol_bot
        if hold_val is not None:
            history[hold_key] = hold_val
        else:
            history.pop(hold_key)
        return sol
    elif isinstance(function, Node):
        if isinstance(function.left, (Polynomial, RationalExpression)):
            function.left = function.left.plug_vars(history)
            sol_left = plug_in_var(function.left, variable, history)
            if isinstance(sol_left, Polynomial):
                if sol_left.get_degree() == 0:
                    sol_left = sol_left.get_coefficients(0)[0]
        else:
            print("not a poly left")
            if hold_val is not None:
                history[hold_key] = hold_val
            else:
                history.pop(hold_key)
            return None
        if isinstance(function.right, (Polynomial, RationalExpression)):
            function.right = function.right.plug_vars(history)
            sol_right = plug_in_var(function.right, variable, history)
            if isinstance(sol_right, Polynomial):
                if sol_right.get_degree() == 0:
                    sol_right = sol_right.get_coefficients(0)[0]
        else:
            print("not a poly right")
            if hold_val is not None:
                history[hold_key] = hold_val
            else:
                history.pop(hold_key)
            return None
        sol = sol_left % sol_right
        if hold_val is not None:
            history[hold_key] = hold_val
        else:
            history.pop(hold_key)
        return sol
    else:
        print("function not poly/rational or otherwise")
    if hold_val is not None:
        history[hold_key] = hold_val
    else:
        history.pop(hold_key)
    return None
