# ============================================================
# Secant Method
# ------------------------------------------------------------
# An open method similar to Newton-Raphson, but it does NOT
# need the derivative. Instead, it approximates the derivative
# using two previous points. You provide two initial guesses
# x0 and x1.
#
# Convergence: ~1.618 (superlinear) — faster than bisection,
# slightly slower than Newton.
# ============================================================

def secant(f, x0, x1, tol=1e-5, max_iter=100):
    """
    Find root of f(x) = 0 using the Secant method.

    Parameters:
        f        : the function f(x)
        x0, x1   : two initial guesses (don't need to bracket the root)
        tol      : tolerance (default 1e-5)
        max_iter : max number of iterations (default 100)

    Returns:
        dict with 'root' and 'steps', or 'error' if something went wrong.
    """
    steps = []

    for i in range(max_iter):
        fx0 = f(x0)
        fx1 = f(x1)

        # The denominator is the approximate derivative
        # If f(x0) == f(x1), the method fails (division by zero)
        if fx1 - fx0 == 0:
            return {"error": "Division by zero — f(x0) equals f(x1). Try different initial guesses."}

        # Secant formula: like Newton's but replaces f'(x) with (f(x1)-f(x0))/(x1-x0)
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

        steps.append({
            "iter": i + 1,
            "x": x2,
            "fx": f(x2),
            "error": abs(x2 - x1)
        })

        # Check if we're close enough
        if abs(x2 - x1) < tol:
            return {"root": x2, "steps": steps}

        # Shift: x0 becomes x1, x1 becomes x2
        x0 = x1
        x1 = x2

    return {"root": x1, "steps": steps}
