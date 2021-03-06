import matplotlib.pyplot as plt
import numpy as np
from typing import List


def bits_to_int_list(bits: str) -> List[int]:
    """
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

    bits = ["phase"] + bits
    print(len(bits), len(signal))
    # vertical lines
    ratio = len(signal)//len(bits)
    vertical_lines_coordinates = np.arange(0, len(signal), ratio)
    for x_pos in vertical_lines_coordinates:
        plt.axvline(x=x_pos, **features)

    # axis
    plt.xticks(vertical_lines_coordinates[:-1]+0.5*ratio, bits)
    plt.yticks([0], [0])

    x_coordinates = list(range(len(signal)))
    plt.step(x_coordinates, signal, where='pre', color='red')

    # scale
    limit = 3
    plt.ylim(bottom=-limit, top=limit)

    plt.title(title)

    plt.show()


def manchester(bits: str, convention: str = "thomas") -> None:
    """Plots the graphical representation of the signal with the manchester
    encoding, can use both Thomas or IEEE convention"""
    bits = bits_to_int_list(bits)

    up_transition = [-1, 1]
    down_transition = [1, -1]

    if convention == 'thomas':
        one, zero = down_transition, up_transition
    elif convention == "ieee":
        one, zero = up_transition, down_transition
    else:
        raise ValueError(f"Convention {convention} does not exist")

    signal = []
    for bit in bits:
        if bit:
            signal += one
        else:
            signal += zero

    signal = [0]*3 + signal
    make_graph(signal, bits, f"{convention.upper()} Manchester Representation")


def d_manchester(bits: str, initial_state=-1) -> None:
    """Plots the graphical representation of the signal with the differential
    manchester encoding"""
    bits = bits_to_int_list(bits)

    signal = []
    phase = initial_state

    for bit in bits:
        if bit:
            signal.append(phase)
            phase *= -1
            signal.append(phase)
        else:
            signal.append(phase * -1)
            signal.append(phase)

    signal = [initial_state]*3 + signal

    title = "Differential Manchester Representation"
    make_graph(signal, bits, title)


def b8zs(bits: str, initial_state: int = -1) -> None:
    """Plots the graphical representation of the signal with the binary eight
    zero suppress encodings, can change the initial phase to 0 or 1"""
    bits = bits_to_int_list(bits)

    signal = []
    phase = initial_state

    count_zero = 0
    for bit in bits:
        if bit == 1:
            phase *= -1
            signal.append(phase)
            count_zero = 0
        elif bit == 0:
            signal.append(0)
            count_zero += 1
            if count_zero == 8:
                signal[-5:] = [phase, phase*-1, 0, phase*-1, phase]
                count_zero = 0

    signal = [initial_state]*2 + signal
    title = "B8ZS representation"
    make_graph(signal, bits, title)


def is_even(number: int):
    """Return True if the number is even and false otherwise"""
    return number % 2 == 0


def four_zeros_substitution(count_pulses: int, phase: int) -> List[int]:
    """returns the modified values based on the table rule of hdb3"""

    count_pulses_even = (count_pulses % 2 == 0)
    state_positive = (phase == 1)
    if count_pulses_even and state_positive:
        modified = [-1, 0, 0, -1]
    elif count_pulses_even and not state_positive:
        modified = [1, 0, 0, 1]
    elif not count_pulses_even and state_positive:
        modified = [0, 0, 0, 1]
    else:
        modified = [0, 0, 0, -1]
    return modified


def hdb3(bits: str, initial_state: int) -> None:
    """Plots the graphical representation of the signal with the HDB3 encoding,
     can change the initial phase to 0 or 1"""
    bits = bits_to_int_list(bits)

    signal = []
    phase = initial_state

    count_zero = 0
    count_pulses = 1  # because of phase

    for bit in bits:

        if bit == 1:
            phase *= -1
            signal.append(phase)
            count_pulses += 1
            count_zero = 0

        elif bit == 0:
            count_zero += 1
            signal.append(0)

            if count_zero == 4:
                signal[-4:] = four_zeros_substitution(count_pulses, phase)
                phase = signal[-1]
                count_pulses = 0
                count_zero = 0

    signal = [initial_state]*2 + signal
    title = "HDB3 Representation"
    make_graph(signal, bits, title)
