import matplotlib.pyplot as plt
import numpy as np
from typing import List
from datetime import datetime

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

    bits = ["State"] + bits
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

    plt.savefig(f"{datetime.now().isoformat()}.png")
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

    signal = [0]*3 + signal
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

    signal = [initial_state]*3 + signal

    alternate_string = "Aternate " if alternate else ""
    title = f"{alternate_string}Differential Manchester Representation"
    make_graph(signal, bits, title)


def b8zs(bits:str, initial_state: int = -1) -> None:
    """Plots the graphical representation of the signal with the binary eight
    zero suppress encodings, can change the initial state to 0 or 1"""
    bits = bits_to_int_list(bits)

    signal = []
    state = initial_state

    count_zero = 1 if state == 0 else 0
    for index in range(len(bits)):
        if bits[index]:
            state *= -1
            signal.append(state)
        else:
            count_zero += 1
            if count_zero == 8:
                count_zero = 0
                signal[-4] = state
                signal[-3] = state * -1
                signal[-2] = 0
                signal[-1] = state * -1
                signal.append(state)
            else:
                signal.append(0)

    signal = [initial_state]*2 + signal
    title = "B8ZS representation"
    make_graph(signal, bits, title)


def is_even(number: int):
    """Return True if the number is even and false otherwise"""
    return number % 2 == 0


def hdb3(bits: str, initial_state: int = -1) -> None:
    """Plots the graphical representation of the signal with the HDB3 encoding,
     can change the initial state to 0 or 1"""
    bits = bits_to_int_list(bits)

    signal = []
    state = initial_state

    count_zero = 0
    count_one_since_last_substitution = 1  # because of state
    preceding_pulse = state
    for index in range(len(bits)):
        if bits[index]:
            state *= -1
            signal.append(state)
            count_one_since_last_substitution += 1
            preceding_pulse = state
            count_zero = 0
        else:
            count_zero += 1
            if count_zero == 4:
                is_count_one_even = count_one_since_last_substitution % 2 == 0
                is_preceding_pulse_positive = preceding_pulse == 1
                if is_count_one_even and is_preceding_pulse_positive:
                    change = [-1, 0, 0]
                    to_add = -1
                elif is_count_one_even and not is_preceding_pulse_positive:
                    change = [1, 0, 0]
                    to_add = 1
                elif not is_count_one_even and is_preceding_pulse_positive:
                    change = [0, 0, 0]
                    to_add = 1
                else:
                    change = [0, 0, 0]
                    to_add = -1
                signal[-3:] = change.copy()
                signal.append(to_add)
                state = signal[-1]
                count_one_since_last_substitution = 0
                preceding_pulse = state
                count_zero = 0
            else:
                signal.append(0)

    signal = [initial_state]*2 + signal
    title = "HDB3 Representation"
    make_graph(signal, bits, title)

number = "00000000011001100001"
manchester(number)
manchester(number, convention="ieee")
d_manchester(number, initial_state=-1)
d_manchester(number, initial_state=1)
d_manchester(number, alternate=True, initial_state=-1)
d_manchester(number, alternate=True, initial_state=1)
b8zs(number, initial_state=1)
b8zs(number, initial_state=-1)
hdb3(number, initial_state=1)
hdb3(number, initial_state=-1)





