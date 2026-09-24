# IPv4 Int Converter

Convert IPv4 addresses between dotted-quad strings and packed 32-bit unsigned integers.

```python
from ipv4_int_converter import ipv4_to_int, int_to_ipv4

# String to integer
addr_int = ipv4_to_int("192.168.1.1")
print(addr_int)  # 3232235777

# Integer back to string
addr_str = int_to_ipv4(3232235777)
print(addr_str)  # "192.168.1.1"
```

## Why this library exists

Network code frequently needs to store or compare IPv4 addresses as integers, for example when sorting, hashing, or doing bitwise operations. This package provides the two small conversion functions that every such project ends up writing by hand, with strict input validation and no dependencies beyond the Python standard library.

The trade-off made here is strictness. Addresses with leading zero octets (for example `"192.168.001.001"`) are rejected rather than interpreted, because leading zeros are a well-known source of ambiguity in IP address parsing. If you need lenient parsing, this library is not the right tool.

## Awkward edge

Both functions raise `ValueError` for out-of-range or malformed input, and `TypeError` when the argument has the wrong type. `bool` is accepted by `int_to_ipv4` because it is a subclass of `int` in Python.
