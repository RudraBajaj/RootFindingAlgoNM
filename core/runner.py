from methods.bisection import bisection
from methods.newton import newton
from methods.regula_falsi import regula_falsi
from methods.secant import secant
from methods.modified_newton import modified_newton


def run_method(method_name, f, df=None, d2f=None, params={}):
    """
    Traffic controller — picks the right method and calls it with the right params.

    Parameters:
        method_name : which method to use (string)
        f           : the function f(x)
        df          : first derivative f'(x)   (for Newton, Modified Newton)
        d2f         : second derivative f''(x)  (for Modified Newton)
        params      : dict of parameters (a, b, x0, x1 depending on method)

    Returns:
        dict with 'root' and 'steps', or 'error' message.
    """
    if method_name == "bisection":
        return bisection(f, params["a"], params["b"])

    elif method_name == "newton":
        return newton(f, df, params["x0"])

    elif method_name == "regula_falsi":
        return regula_falsi(f, params["a"], params["b"])

    elif method_name == "secant":
        return secant(f, params["x0"], params["x1"])

    elif method_name == "modified_newton":
        return modified_newton(f, df, d2f, params["x0"])

    else:
        return {"error": "Unknown method"}