def newton(f, df, x0, tol=1e-5, max_iter=100):
    steps = []

    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)

        if dfx == 0:
            return {"error": "Zero derivative"}

        x_new = x - fx / dfx

        steps.append({
            "iter": i,
            "x": x_new,
            "fx": f(x_new),
            "error": abs(x_new - x)
        })

        if abs(x_new - x) < tol:
            return {"root": x_new, "steps": steps}

        x = x_new

    return {"root": x, "steps": steps}