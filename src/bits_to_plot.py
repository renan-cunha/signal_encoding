import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple


def bits_to_int_list(bits: str) -> List[int]:
    """Bits to list representation
    Ex:
        1010100 -> [1, 0, 1, 0, 1, 0, 0]
    """
    bits = list(map(int, bits))
    return bits


def make_graph(signal: List[int], bits: List[int], title: str) -> None:
    """Uses matplotlib.pyplot step method to make signal representation"""

    # horizontal lines
    features = {'color': 'gray', 'linewidth': 0.4}
    plt.axhline(y=0, **features)

    # vertical lines
    vertical_lines_coordinates = np.arange(0, len(signal), 2) + 0.5
    for x_pos in vertical_lines_coordinates:
        plt.axvline(x=x_pos, **features)

    # axis
    plt.xticks(vertical_lines_coordinates + 1, bits)
    plt.yticks([0], [0])

    x_coordinates = list(range(len(signal)))
    plt.step(x_coordinates, signal, where='mid', color='red')

    # scale
    plt.ylim(bottom=-1.5, top=1.5)

    plt.title(title)

    plt.show()


def manchester(bits: str, convention: str = "thomas") -> None:
    """Plots the graphical representation of the signal with the manchester
    encoding, ca use the Thomas or IEEE convention"""
    bits = bits_to_int_list(bits)

    if convention == 'thomas':
        positive, negative = 1, -1
    elif convention == "ieee":
        positive, negative = -1, 1
    else:
        raise ValueError(f"Convention {convention} does not exist")

    signal = []
    for bit in bits:
        if bit:
            signal += [positive, negative]
        else:
            signal += [negative, positive]

    signal = [0] + signal + [0]
    make_graph(signal, bits, f"{convention.upper()} Manchester Representation")


def d_manchester(bits: str, alternate: bool = False, initial_state=-1) -> None:
    """Plots the graphical representation of the signal with the differential
    manchester encoding, cna use the default or the alternate convention"""
    bits = bits_to_int_list(bits)

    signal = []
    state = initial_state

    for bit in bits:
        if bit != alternate:
            signal.append(state * -1)
            signal.append(state)
        else:
            signal.append(state)
            state *= -1
            signal.append(state)

    signal = [initial_state] + signal + [initial_state]
    alternate_string = "Aternate " if alternate else ""
    title = f"{alternate_string}Differential Manchester Representation"
    make_graph(signal, bits, title)


manchester("10100111001")
manchester("10100111001", convention="ieee")
d_manchester('101001110010')
d_manchester('101001110010', alternate=True)