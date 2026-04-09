def bisection(f, a, b, tol=1e-5, max_iter=100):
    steps = []

    if f(a) * f(b) >= 0:
        return {"error": "Invalid interval"}

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        steps.append({
            "iter": i,
            "x": c,
            "fx": fc,
            "error": abs(b - a)
        })

        if abs(fc) < tol:
            return {"root": c, "steps": steps}

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return {"root": c, "steps": steps}