import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def parse_function(expr_str):
    """
    Takes a math expression string like "x**2 - 4" and converts it into
    callable Python functions.

    Returns:
        f   : the function f(x)
        df  : the first derivative f'(x)
        d2f : the second derivative f''(x)  (needed for Modified Newton)
    """
    x = sp.symbols('x')

    # Allow implicit multiplication like "2x" instead of "2*x"
    transformations = standard_transformations + (implicit_multiplication_application,)

    expr = parse_expr(expr_str, transformations=transformations)

    # Create callable functions from the symbolic expression
    f = sp.lambdify(x, expr, "math")                    # f(x)
    df = sp.lambdify(x, sp.diff(expr, x), "math")       # f'(x)
    d2f = sp.lambdify(x, sp.diff(expr, x, 2), "math")   # f''(x)

    return f, df, d2f