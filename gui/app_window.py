import tkinter as tk
from tkinter import ttk, messagebox
from core.parser import parse_function
from core.runner import run_method
from utils.plotter import plot_function
from utils.validator import validate_equation, validate_params


def run_app():
    # ============================================================
    # SOLVE button callback — runs the selected method
    # ============================================================
    def solve():
        try:
            expr = entry.get()
            method = method_var.get()

            # Step 1: Validate the equation
            eq_valid, eq_error = validate_equation(expr)
            if not eq_valid:
                messagebox.showerror("Invalid Equation", eq_error)
                output.config(text="Fix the equation and try again.", foreground="red")
                return

            # Step 2: Parse the equation into f(x), f'(x), f''(x)
            f, df, d2f = parse_function(expr)

            # Step 3: Validate the parameters
            param_valid, params, param_error = validate_params(
                method, param1_entry.get(), param2_entry.get(), f
            )
            if not param_valid:
                messagebox.showerror("Invalid Parameters", param_error)
                output.config(text="Fix the parameters and try again.", foreground="red")
                return

            # Step 4: Run the selected method
            if method in ("bisection", "regula_falsi"):
                result = run_method(method, f, params=params)
            elif method == "newton":
                result = run_method(method, f, df, params=params)
            elif method == "secant":
                result = run_method(method, f, params=params)
            elif method == "modified_newton":
                result = run_method(method, f, df, d2f, params=params)
            else:
                result = {"error": "Unknown method selected."}

            # Step 5: Display result
            if "error" in result:
                output.config(text=f"Error: {result['error']}", foreground="red")
                clear_table()
            else:
                root_val = result['root']
                steps = result.get('steps', [])
                iterations = len(steps)
                output.config(
                    text=f"Root Found: {root_val:.6f}  ({iterations} iterations)",
                    foreground="#007F00"
                )
                # Fill the iteration table
                fill_table(steps, method)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate:\n{str(e)}")
            output.config(text="Waiting for valid input...", foreground="gray")

    # ============================================================
    # PLOT button callback — draws the graph
    # ============================================================
    def plot():
        try:
            expr = entry.get()

            # Validate the equation first
            eq_valid, eq_error = validate_equation(expr)
            if not eq_valid:
                messagebox.showerror("Invalid Equation", eq_error)
                return

            plot_function(parse_function(expr)[0])
        except Exception as e:
            messagebox.showerror("Plotting Error", f"Failed to plot function:\n{str(e)}")

    # ============================================================
    # Step-by-step iteration table functions
    # ============================================================
    def clear_table():
        """Remove all rows from the table."""
        for item in steps_tree.get_children():
            steps_tree.delete(item)

    def fill_table(steps, method):
        """Fill the iteration table with step-by-step data."""
        clear_table()

        # Configure columns based on method type
        if method in ("bisection", "regula_falsi"):
            steps_tree["columns"] = ("iter", "a", "b", "x", "fx", "error")
            steps_tree.heading("iter", text="Iter")
            steps_tree.heading("a", text="a")
            steps_tree.heading("b", text="b")
            steps_tree.heading("x", text="x (root approx)")
            steps_tree.heading("fx", text="f(x)")
            steps_tree.heading("error", text="|f(x)|")

            steps_tree.column("iter", width=40, anchor=tk.CENTER)
            steps_tree.column("a", width=90, anchor=tk.CENTER)
            steps_tree.column("b", width=90, anchor=tk.CENTER)
            steps_tree.column("x", width=120, anchor=tk.CENTER)
            steps_tree.column("fx", width=120, anchor=tk.CENTER)
            steps_tree.column("error", width=100, anchor=tk.CENTER)

            for step in steps:
                steps_tree.insert("", tk.END, values=(
                    step["iter"],
                    f"{step.get('a', '-'):.6f}" if isinstance(step.get('a'), (int, float)) else "-",
                    f"{step.get('b', '-'):.6f}" if isinstance(step.get('b'), (int, float)) else "-",
                    f"{step['x']:.6f}",
                    f"{step['fx']:.6f}",
                    f"{step['error']:.6f}"
                ))
        else:
            # Newton, Secant, Modified Newton — no a, b columns
            steps_tree["columns"] = ("iter", "x", "fx", "error")
            steps_tree.heading("iter", text="Iter")
            steps_tree.heading("x", text="x (root approx)")
            steps_tree.heading("fx", text="f(x)")
            steps_tree.heading("error", text="|xₙ - xₙ₋₁|")

            steps_tree.column("iter", width=50, anchor=tk.CENTER)
            steps_tree.column("x", width=160, anchor=tk.CENTER)
            steps_tree.column("fx", width=160, anchor=tk.CENTER)
            steps_tree.column("error", width=130, anchor=tk.CENTER)

            for step in steps:
                steps_tree.insert("", tk.END, values=(
                    step["iter"],
                    f"{step['x']:.6f}",
                    f"{step['fx']:.6f}",
                    f"{step['error']:.6f}"
                ))

    # ============================================================
    # Update input fields when user switches method
    # ============================================================
    def update_params_ui(*args):
        method = method_var.get()

        if method in ("bisection", "regula_falsi"):
            # Show two fields: a and b
            param1_label.config(text="Start 'a':")
            param2_label.config(text="End 'b':")
            param2_label.grid()
            param2_entry.grid()
            # Reset defaults
            param1_entry.delete(0, tk.END)
            param1_entry.insert(0, "1.0")
            param2_entry.delete(0, tk.END)
            param2_entry.insert(0, "5.0")

        elif method == "secant":
            # Show two fields: x0 and x1
            param1_label.config(text="Guess 'x0':")
            param2_label.config(text="Guess 'x1':")
            param2_label.grid()
            param2_entry.grid()
            # Reset defaults
            param1_entry.delete(0, tk.END)
            param1_entry.insert(0, "1.0")
            param2_entry.delete(0, tk.END)
            param2_entry.insert(0, "3.0")

        else:
            # Newton / Modified Newton — just one field: x0
            param1_label.config(text="Guess 'x0':")
            param2_label.grid_remove()
            param2_entry.grid_remove()
            param1_entry.delete(0, tk.END)
            param1_entry.insert(0, "2.0")

    # ============================================================
    # BUILD THE WINDOW
    # ============================================================
    root = tk.Tk()
    root.title("Numerical Methods — Non-Linear Equation Root Finder")
    root.geometry("650x600")
    root.resizable(True, True)
    root.minsize(550, 500)

    # --- Styling ---
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')

    style.configure('TLabel', font=('Segoe UI', 11))
    style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6)
    style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'))
    style.configure('Treeview', font=('Consolas', 10), rowheight=24)
    style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))

    main_frame = ttk.Frame(root, padding="20 15 20 15")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # --- Title ---
    ttk.Label(main_frame, text="Equation Root Finder", style="Header.TLabel").pack(pady=(0, 15))

    # --- Equation input ---
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill=tk.X, pady=5)

    ttk.Label(input_frame, text="f(x) = ").pack(side=tk.LEFT)
    entry = ttk.Entry(input_frame, width=30, font=('Segoe UI', 12))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
    entry.insert(0, "x**2 - 4")

    # --- Method dropdown ---
    method_frame = ttk.Frame(main_frame)
    method_frame.pack(fill=tk.X, pady=10)

    ttk.Label(method_frame, text="Method:").pack(side=tk.LEFT)
    method_var = tk.StringVar(value="bisection")

    all_methods = ["bisection", "regula_falsi", "newton", "secant", "modified_newton"]
    method_dropdown = ttk.Combobox(
        method_frame,
        textvariable=method_var,
        values=all_methods,
        state="readonly",
        width=20
    )
    method_dropdown.pack(side=tk.LEFT, padx=(10, 0))

    # --- Parameter inputs ---
    params_frame = ttk.Frame(main_frame)
    params_frame.pack(fill=tk.X, pady=5)

    param1_label = ttk.Label(params_frame, text="Start 'a':")
    param1_label.grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
    param1_entry = ttk.Entry(params_frame, width=10, font=('Segoe UI', 11))
    param1_entry.grid(row=0, column=1, padx=(0, 15))
    param1_entry.insert(0, "1.0")

    param2_label = ttk.Label(params_frame, text="End 'b':")
    param2_label.grid(row=0, column=2, padx=(0, 5), sticky=tk.W)
    param2_entry = ttk.Entry(params_frame, width=10, font=('Segoe UI', 11))
    param2_entry.grid(row=0, column=3)
    param2_entry.insert(0, "5.0")

    # Listen for method changes
    method_var.trace_add("write", update_params_ui)

    # --- Buttons ---
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=10)

    ttk.Button(button_frame, text="Solve Root", command=solve).pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
    ttk.Button(button_frame, text="Plot Graph", command=plot).pack(side=tk.LEFT, fill=tk.X, expand=True)

    # --- Output label ---
    output = ttk.Label(main_frame, text="Waiting for input...", font=('Segoe UI', 12, 'italic'), foreground="gray")
    output.pack(pady=(8, 8))

    # --- Separator ---
    ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 5))

    # --- Iteration Steps Table ---
    table_label = ttk.Label(main_frame, text="Step-by-Step Iterations:", font=('Segoe UI', 11, 'bold'))
    table_label.pack(anchor=tk.W)

    # Table frame with scrollbar
    table_frame = ttk.Frame(main_frame)
    table_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    # Scrollbar
    table_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
    table_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # Treeview (the table itself)
    steps_tree = ttk.Treeview(
        table_frame,
        columns=("iter", "x", "fx", "error"),
        show="headings",
        height=8,
        yscrollcommand=table_scroll.set
    )
    steps_tree.pack(fill=tk.BOTH, expand=True)
    table_scroll.config(command=steps_tree.yview)

    # Default column headers
    steps_tree.heading("iter", text="Iter")
    steps_tree.heading("x", text="x (root approx)")
    steps_tree.heading("fx", text="f(x)")
    steps_tree.heading("error", text="Error")

    steps_tree.column("iter", width=50, anchor=tk.CENTER)
    steps_tree.column("x", width=160, anchor=tk.CENTER)
    steps_tree.column("fx", width=160, anchor=tk.CENTER)
    steps_tree.column("error", width=130, anchor=tk.CENTER)

    # Alternating row colors for readability
    steps_tree.tag_configure('oddrow', background='#f0f0f0')
    steps_tree.tag_configure('evenrow', background='#ffffff')

    root.mainloop()