import matplotlib.pyplot as plt
import numpy as np


def nrz(bits: str) -> None:
    """Plots the graphical representation with the non return to zero
    enconding"""
    bits = list(bits)
    bits = list(map(int, bits))

    bits.append(bits[-1])
    x = list(range(len(bits)))

    plt.axhline(y=1 / 2, color='gray', linestyle=":")

    for i in x:
        plt.axvline(x=i, color='gray', linestyle=":")
    plt.step(list(range(len(bits))), bits, where='post')

    plt.xticks(np.array(x[:-1])+0.5, bits)
    plt.yticks([1/2], [0])
    plt.ylim(bottom=-0.25, top=1.25)
    plt.show()

