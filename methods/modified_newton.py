# ============================================================
# Modified Newton-Raphson Method
# ------------------------------------------------------------
# Regular Newton-Raphson struggles with repeated (multiple)
# roots because convergence slows down to linear.
#
# This modified version uses both f'(x) and f''(x) to fix
# that problem, restoring quadratic convergence even for
# repeated roots.
#
# Formula: x_new = x - (f(x) * f'(x)) / (f'(x)^2 - f(x) * f''(x))
# ============================================================

def modified_newton(f, df, d2f, x0, tol=1e-5, max_iter=100):
    """
    Find root of f(x) = 0 using Modified Newton-Raphson method.

    Parameters:
        f        : the function f(x)
        df       : first derivative f'(x)
        d2f      : second derivative f''(x)
        x0       : initial guess
        tol      : tolerance (default 1e-5)
        max_iter : max number of iterations (default 100)

    Returns:
        dict with 'root' and 'steps', or 'error' if something went wrong.
    """
    steps = []
    x = x0

    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        d2fx = d2f(x)

        # Denominator: f'(x)^2 - f(x)*f''(x)
        denominator = dfx**2 - fx * d2fx

        if denominator == 0:
            return {"error": "Zero denominator — method cannot continue at this point."}

        # Modified Newton formula
        x_new = x - (fx * dfx) / denominator

        steps.append({
            "iter": i + 1,
            "x": x_new,
            "fx": f(x_new),
            "error": abs(x_new - x)
        })

        # Check convergence
        if abs(x_new - x) < tol:
            return {"root": x_new, "steps": steps}

        x = x_new

    return {"root": x, "steps": steps}
