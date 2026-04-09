# ============================================================
# Input Validator
# ------------------------------------------------------------
# Checks all user inputs BEFORE solving and gives clear,
# helpful error messages explaining exactly what went wrong
# and how to fix it.
# ============================================================

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application


def validate_equation(expr_str):
    """
    Checks if the equation string is valid.

    Returns:
        (True, None)           — if valid
        (False, error_message) — if invalid, with a helpful reason
    """
    # Check 1: Is the field empty?
    if not expr_str or not expr_str.strip():
        return False, "The equation field is empty.\n\nPlease enter a function like: x**2 - 4"

    expr_str = expr_str.strip()

    # Check 2: Did the user use ^ instead of **?
    if "^" in expr_str:
        return False, (
            f"You used '^' for power, but Python uses '**'.\n\n"
            f"Fix: Replace '{expr_str}' with '{expr_str.replace('^', '**')}'"
        )

    # Check 3: Does it use a variable other than x?
    try:
        transformations = standard_transformations + (implicit_multiplication_application,)
        parsed = parse_expr(expr_str, transformations=transformations)
        symbols_used = parsed.free_symbols
        x = sp.Symbol('x')

        if len(symbols_used) == 0:
            return False, (
                f"Your input '{expr_str}' is just a number, not an equation.\n\n"
                f"Enter a function of x, like: x**2 - 4"
            )

        if symbols_used != {x}:
            wrong_vars = ", ".join(str(s) for s in symbols_used if s != x)
            return False, (
                f"Your equation uses variable(s): {wrong_vars}\n\n"
                f"Only 'x' is allowed. Example: x**2 - 4"
            )

    except Exception:
        return False, (
            f"Could not understand '{expr_str}' as a math expression.\n\n"
            f"Valid examples:\n"
            f"  • x**2 - 4\n"
            f"  • sin(x) - 0.5\n"
            f"  • exp(x) - 3\n"
            f"  • x**3 - 2*x + 1"
        )

    return True, None


def validate_params(method, param1_str, param2_str, f=None):
    """
    Checks if the parameter inputs are valid for the selected method.

    Returns:
        (True, params_dict, None)    — if valid
        (False, None, error_message) — if invalid, with a helpful reason
    """

    # --- Methods that need interval [a, b] ---
    if method in ("bisection", "regula_falsi"):
        # Check: are a and b numbers?
        try:
            a = float(param1_str)
        except (ValueError, TypeError):
            return False, None, (
                f"Parameter 'a' = '{param1_str}' is not a valid number.\n\n"
                f"Enter a number like: 1.0, -3, 0.5"
            )

        try:
            b = float(param2_str)
        except (ValueError, TypeError):
            return False, None, (
                f"Parameter 'b' = '{param2_str}' is not a valid number.\n\n"
                f"Enter a number like: 5.0, -1, 2.5"
            )

        # Check: a and b should be different
        if a == b:
            return False, None, (
                f"'a' and 'b' are both {a}. They must be different.\n\n"
                f"The interval needs a start and end point, like a=1, b=5."
            )

        # Check: a should be less than b
        if a > b:
            a, b = b, a  # auto-fix, but we still check signs

        # Check: f(a) and f(b) must have opposite signs
        if f is not None:
            try:
                fa = f(a)
                fb = f(b)
                if fa * fb > 0:
                    sign_a = "positive" if fa > 0 else "negative"
                    sign_b = "positive" if fb > 0 else "negative"
                    return False, None, (
                        f"f(a) = f({a}) = {fa:.4f} ({sign_a})\n"
                        f"f(b) = f({b}) = {fb:.4f} ({sign_b})\n\n"
                        f"Both have the SAME sign! For {method.replace('_', ' ').title()}, "
                        f"f(a) and f(b) must have OPPOSITE signs "
                        f"(one positive, one negative).\n\n"
                        f"This means there may be no root in [{a}, {b}]. "
                        f"Try a wider interval."
                    )
                if fa == 0:
                    return True, {"a": a, "b": b, "root_at_a": True}, None
                if fb == 0:
                    return True, {"a": a, "b": b, "root_at_b": True}, None
            except Exception as e:
                return False, None, (
                    f"Could not evaluate f(x) at a={a} or b={b}.\n\n"
                    f"Reason: {str(e)}\n\n"
                    f"The function may not be defined at these points "
                    f"(e.g., log(x) at x ≤ 0)."
                )

        return True, {"a": a, "b": b}, None

    # --- Newton and Modified Newton need x0 ---
    elif method in ("newton", "modified_newton"):
        try:
            x0 = float(param1_str)
        except (ValueError, TypeError):
            return False, None, (
                f"Parameter 'x0' = '{param1_str}' is not a valid number.\n\n"
                f"Enter an initial guess like: 2.0, -1, 0.5"
            )

        # Check: can we evaluate f at x0?
        if f is not None:
            try:
                f(x0)
            except Exception as e:
                return False, None, (
                    f"Cannot evaluate f(x) at x0 = {x0}.\n\n"
                    f"Reason: {str(e)}\n\n"
                    f"The function may not be defined here "
                    f"(e.g., log(x) at x ≤ 0, or 1/x at x = 0)."
                )

        return True, {"x0": x0}, None

    # --- Secant needs x0 and x1 ---
    elif method == "secant":
        try:
            x0 = float(param1_str)
        except (ValueError, TypeError):
            return False, None, (
                f"Parameter 'x0' = '{param1_str}' is not a valid number.\n\n"
                f"Enter a number like: 1.0, -3, 0.5"
            )

        try:
            x1 = float(param2_str)
        except (ValueError, TypeError):
            return False, None, (
                f"Parameter 'x1' = '{param2_str}' is not a valid number.\n\n"
                f"Enter a number like: 3.0, -1, 2.5"
            )

        # Check: x0 and x1 must be different
        if x0 == x1:
            return False, None, (
                f"x0 and x1 are both {x0}. They must be DIFFERENT.\n\n"
                f"The Secant method needs two distinct points to draw a line.\n"
                f"Try: x0 = 1.0, x1 = 3.0"
            )

        # Check: can we evaluate f at both?
        if f is not None:
            try:
                fx0 = f(x0)
                fx1 = f(x1)
                if fx0 == fx1:
                    return False, None, (
                        f"f(x0) = f(x1) = {fx0:.4f}\n\n"
                        f"Both points give the same f(x) value, so the secant "
                        f"line would be horizontal (slope = 0) — division by zero!\n\n"
                        f"Try different guesses where f(x0) ≠ f(x1)."
                    )
            except Exception as e:
                return False, None, (
                    f"Cannot evaluate f(x) at x0={x0} or x1={x1}.\n\n"
                    f"Reason: {str(e)}\n\n"
                    f"The function may not be defined at these points."
                )

        return True, {"x0": x0, "x1": x1}, None

    else:
        return False, None, f"Unknown method: '{method}'"
