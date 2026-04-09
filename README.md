# 🔢 Numerical Methods — Non-Linear Equation Root Finder

A Python GUI application for solving non-linear equations using 5 different numerical methods. Built with `tkinter` for the interface and `sympy` for symbolic math.

---

## 📋 Features

- **5 Root-Finding Methods**: Bisection, Regula Falsi, Newton-Raphson, Secant, Modified Newton-Raphson
- **Step-by-Step Iteration Table**: See every iteration with x, f(x), and error values
- **Graph Plotting**: Visualize your function with matplotlib
- **Smart Input Validation**: Clear error messages that explain what went wrong and how to fix it
- **Dynamic UI**: Input fields change automatically based on the selected method

---

## 🚀 How to Run

### 1. Install Python
Make sure you have Python 3.10+ installed.

### 2. Install Dependencies
```bash
pip install sympy matplotlib numpy
```

### 3. Run the App
```bash
python main.py
```

---

## 📁 Project Structure

```
Nm project sem 6/
├── main.py                          ← Run this to start the app
├── README.md                        ← You are here
│
├── core/                            ← The Brain
│   ├── parser.py                    ← Converts equation string → f(x), f'(x), f''(x)
│   └── runner.py                    ← Picks and calls the right method
│
├── methods/                         ← The Solvers
│   ├── bisection.py                 ← Bisection Method
│   ├── newton.py                    ← Newton-Raphson Method
│   ├── regula_falsi.py              ← Regula Falsi (False Position) Method
│   ├── secant.py                    ← Secant Method
│   └── modified_newton.py           ← Modified Newton-Raphson Method
│
├── gui/                             ← The Screen
│   └── app_window.py                ← Builds the GUI window with iteration table
│
└── utils/                           ← Helper Tools
    ├── plotter.py                   ← Draws function graphs
    └── validator.py                 ← Validates all inputs with helpful error messages
```

---

## 🧮 Methods Explained

### 1. Bisection Method
- **Type**: Bracketing method
- **Inputs**: Interval [a, b] where f(a) and f(b) have opposite signs
- **How it works**: Keeps cutting the interval in half until the root is found
- **Convergence**: Slow but guaranteed

### 2. Regula Falsi (False Position)
- **Type**: Bracketing method
- **Inputs**: Interval [a, b] where f(a) and f(b) have opposite signs
- **How it works**: Draws a line between (a, f(a)) and (b, f(b)), picks the x-intercept
- **Convergence**: Faster than bisection in most cases

### 3. Newton-Raphson
- **Type**: Open method
- **Inputs**: Initial guess x0
- **How it works**: Uses the tangent line (derivative f') to find the next approximation
- **Convergence**: Very fast (quadratic), but needs a good guess

### 4. Secant Method
- **Type**: Open method
- **Inputs**: Two initial guesses x0 and x1
- **How it works**: Like Newton but approximates the derivative using two points
- **Convergence**: Faster than bisection, no derivative needed

### 5. Modified Newton-Raphson
- **Type**: Open method
- **Inputs**: Initial guess x0
- **How it works**: Uses f(x), f'(x), and f''(x) to handle repeated roots
- **Convergence**: Quadratic even for repeated roots (where regular Newton slows down)

---

## ✅ Valid Inputs

### Equation Field — f(x)

| Input | Meaning |
|-------|---------|
| `x**2 - 4` | x² − 4 |
| `x**3 - x - 2` | x³ − x − 2 |
| `sin(x)` | sin(x) |
| `cos(x) - x` | cos(x) − x |
| `exp(x) - 3` | eˣ − 3 |
| `log(x) - 1` | ln(x) − 1 |
| `sqrt(x) - 2` | √x − 2 |
| `(x-1)**2` | (x−1)² — repeated root, use Modified Newton! |

### ❌ Invalid Inputs (with error messages)

| Input | Error You'll See |
|-------|-----------------|
| *(empty)* | "The equation field is empty" |
| `x^2 - 4` | "You used '^' for power, but Python uses '**'" |
| `y**2 - 4` | "Only 'x' is allowed" |
| `42` | "Just a number, not an equation" |
| `hello` | "Could not understand as a math expression" |

---

## 🧪 Testing Guide

### Test 1: Bisection Method
| # | Equation | a | b | Expected Result |
|---|----------|---|---|----------------|
| 1.1 | `x**2 - 4` | 1 | 5 | ✅ Root ≈ 2.000000 |
| 1.2 | `x**3 - x - 2` | 1 | 2 | ✅ Root ≈ 1.521380 |
| 1.3 | `sin(x)` | 2 | 4 | ✅ Root ≈ 3.141593 (π) |
| 1.4 | `x**2 - 4` | 3 | 5 | ❌ Error: same sign |
| 1.5 | `x**2 - 4` | 1 | 1 | ❌ Error: a and b are same |

### Test 2: Regula Falsi
| # | Equation | a | b | Expected Result |
|---|----------|---|---|----------------|
| 2.1 | `x**2 - 4` | 1 | 5 | ✅ Root ≈ 2.000000 |
| 2.2 | `x**3 - 27` | 2 | 4 | ✅ Root ≈ 3.000000 |
| 2.3 | `x**2 - 4` | 3 | 5 | ❌ Error: same sign |

### Test 3: Newton-Raphson
| # | Equation | x0 | Expected Result |
|---|----------|----|----------------|
| 3.1 | `x**2 - 4` | 5 | ✅ Root ≈ 2.000000 |
| 3.2 | `x**2 - 4` | -5 | ✅ Root ≈ -2.000000 |
| 3.3 | `cos(x) - x` | 1 | ✅ Root ≈ 0.739085 |

### Test 4: Secant Method
| # | Equation | x0 | x1 | Expected Result |
|---|----------|----|----|----------------|
| 4.1 | `x**2 - 4` | 1 | 5 | ✅ Root ≈ 2.000000 |
| 4.2 | `exp(x) - 3` | 0 | 2 | ✅ Root ≈ 1.098612 |
| 4.3 | `x**2 - 4` | 2 | 2 | ❌ Error: same guess |

### Test 5: Modified Newton-Raphson
| # | Equation | x0 | Expected Result |
|---|----------|----|----------------|
| 5.1 | `x**2 - 4` | 5 | ✅ Root ≈ 2.000000 |
| 5.2 | `(x-1)**2` | 3 | ✅ Root ≈ 1.000000 (repeated root!) |

### Test 6: Equation Validation
| # | Equation | Expected Error |
|---|----------|---------------|
| 6.1 | *(empty)* | "The equation field is empty" |
| 6.2 | `x^2 - 4` | "You used '^', use '**'" |
| 6.3 | `y**2 - 4` | "Only 'x' is allowed" |
| 6.4 | `42` | "Just a number, not an equation" |

### Test 7: Plot Graph
| # | Equation | Expected |
|---|----------|----------|
| 7.1 | `x**2 - 4` | Parabola crossing x-axis at -2 and 2 |
| 7.2 | `sin(x)` | Sine wave graph |
| 7.3 | *(empty)* | Error popup |

### Test 8: UI Behavior
| # | Select Method | Expected Fields |
|---|--------------|----------------|
| 8.1 | bisection | Start 'a', End 'b' |
| 8.2 | regula_falsi | Start 'a', End 'b' |
| 8.3 | newton | Guess 'x0' only |
| 8.4 | secant | Guess 'x0', Guess 'x1' |
| 8.5 | modified_newton | Guess 'x0' only |

### Test 9: Iteration Table
| # | What to Check | Expected |
|---|--------------|----------|
| 9.1 | Solve with bisection | Table shows: Iter, a, b, x, f(x), error columns |
| 9.2 | Solve with newton | Table shows: Iter, x, f(x), error columns (no a, b) |
| 9.3 | Switch method and solve again | Table updates with new columns and data |
| 9.4 | Error values decrease with each row | Confirms the method is converging |

---

## 🛠️ Dependencies

| Package | What It's Used For |
|---------|-------------------|
| `sympy` | Parsing equations, computing derivatives |
| `matplotlib` | Plotting function graphs |
| `numpy` | Generating x-values for plots |
| `tkinter` | GUI (comes built-in with Python) |

---

## 👨‍💻 Built With

- Python 3.10+
- Tkinter (GUI)
- SymPy (Symbolic Mathematics)
- Matplotlib (Plotting)
