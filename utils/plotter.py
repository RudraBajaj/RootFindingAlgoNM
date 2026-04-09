import matplotlib.pyplot as plt
import numpy as np


def plot_function(f):

    x = np.linspace(-10, 10, 100)
    y = [f(i) for i in x]

    plt.axhline(0)
    plt.plot(x, y)
    
    plt.title("Function Graph")
    plt.show()