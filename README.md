Methods to plot graphical representation of different signal encoding techniques


Encodings:
* Manchester
* Differential Manchester
* B8ZS
* HDB3


To use

```python
from bits_to_plot import manchester, d_manchester, b8zs, hdb3


bits = "10101010101010111"
manchester(bits)
d_manchester(bits)
b8zs(bits)
hdb3(bits)

