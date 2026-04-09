# ============================================================
# Regula Falsi (False Position) Method
# ------------------------------------------------------------
# A bracketing method like Bisection, but smarter.
# Instead of always picking the midpoint, it draws a straight
# line between f(a) and f(b) and picks where that line crosses
# the x-axis. This usually converges faster than Bisection.
#
# Requires: f(a) and f(b) must have opposite signs.
# ============================================================

def regula_falsi(f, a, b, tol=1e-5, max_iter=100):
    """
    Find root of f(x) = 0 in interval [a, b] using False Position method.

    Parameters:
        f        : the function f(x)
        a, b     : interval endpoints (f(a) and f(b) must have opposite signs)
        tol      : how close to zero is "good enough" (default 1e-5)
        max_iter : max number of iterations (default 100)

    Returns:
        dict with 'root' and 'steps', or 'error' if something went wrong.
    """
    steps = []

    fa = f(a)
    fb = f(b)

    # Check: the signs must be opposite (one positive, one negative)
    if fa * fb >= 0:
        return {"error": "Invalid interval — f(a) and f(b) must have opposite signs."}

    for i in range(max_iter):
        # The key formula: weighted average based on function values
        # This gives the x-intercept of the line connecting (a, f(a)) and (b, f(b))
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)

        steps.append({
            "iter": i + 1,
            "a": a,
            "b": b,
            "x": c,
            "fx": fc,
            "error": abs(fc)
        })

        # If f(c) is close enough to zero, we found the root
        if abs(fc) < tol:
            return {"root": c, "steps": steps}

        # Narrow the interval: keep the side where the sign changes
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return {"root": c, "steps": steps}
