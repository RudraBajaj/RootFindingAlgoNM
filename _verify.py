import tkinter as tk
from tkinter import ttk

# Quick test: verify Treeview works
root = tk.Tk()
root.withdraw()
tree = ttk.Treeview(root, columns=('a','b','c'), show='headings')
tree.heading('a', text='Test')
print('GUI with Treeview table: OK')
root.destroy()

# Verify all methods still work
from core.parser import parse_function
from core.runner import run_method

f, df, d2f = parse_function('x**2 - 4')

r = run_method('bisection', f, params={'a': 1.0, 'b': 5.0})
print('Bisection steps:', len(r['steps']), '| root:', round(r['root'], 6))
print('Bisection step keys:', list(r['steps'][0].keys()))

r2 = run_method('newton', f, df, params={'x0': 5.0})
print('Newton steps:', len(r2['steps']), '| root:', round(r2['root'], 6))
print('Newton step keys:', list(r2['steps'][0].keys()))

print('All checks passed!')
