"""Core conversion functions for IPv4 addresses.

This module provides two functions:

* ``ipv4_to_int`` - dotted-quad string to unsigned 32-bit integer
* ``int_to_ipv4`` - unsigned 32-bit integer to dotted-quad string

Design choices
--------------

The integer representation is an *unsigned* 32-bit value in the range
``0 <= value <= 4294967295``.  This matches the natural way addresses are
viewed as bit strings and avoids any ambiguity about signedness.  Users who
need a signed representation can apply ``struct.pack('>I', value)`` or
``value - 2**32`` themselves.

Input validation is deliberately strict.  Malformed addresses raise
``ValueError`` immediately rather than being silently coerced, because a
converter that guesses about user intent is dangerous in network tooling.
"""

from __future__ import annotations

import re
from typing import Union

# Pre-compiled pattern for the dotted-quad form.  Each octet is restricted
# to 0-255 without any leading-sign handling.  A regex is used instead of
# ``str.split`` because it also rejects empty octets, extra dots, and
# non-numeric characters in one pass.
_IPV4_PATTERN = re.compile(
    r"^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
    r"\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
    r"\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
    r"\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"
)


def ipv4_to_int(address: str) -> int:
    """Convert a dotted-quad IPv4 address to an unsigned 32-bit integer.

    Parameters
    ----------
    address:
        A string of the form ``a.b.c.d`` where each component is a decimal
        integer in the inclusive range 0-255.  Leading zeros are *not*
        permitted; ``"192.168.001.001"`` is rejected because octal-style
        ambiguity is a real source of bugs.

    Returns
    -------
    int
        An unsigned integer in the range ``0 <= value <= 4294967295``.

    Raises
    ------
    TypeError
        If ``address`` is not a string.
    ValueError
        If ``address`` is not a valid dotted-quad IPv4 address.

    Examples
    --------
    >>> ipv4_to_int("0.0.0.0")
    0
    >>> ipv4_to_int("255.255.255.255")
    4294967295
    >>> ipv4_to_int("192.168.1.1")
    3232235777
    """
    if not isinstance(address, str):
        raise TypeError("address must be a string")

    if not _IPV4_PATTERN.match(address):
        raise ValueError(f"invalid IPv4 address: {address!r}")

    octets = address.split(".")
    value = 0
    for octet in octets:
        value = (value << 8) | int(octet)
    return value


def int_to_ipv4(value: int) -> str:
    """Convert an unsigned 32-bit integer to a dotted-quad IPv4 address.

    Parameters
    ----------
    value:
        An integer in the inclusive range 0-4294967295.

    Returns
    -------
    str
        A dotted-quad string such as ``"192.168.1.1"``.  The string always
        contains exactly four decimal octets with no leading zeros.

    Raises
    ------
    TypeError
        If ``value`` is not an integer (``bool`` is an integer subclass and
        is accepted).
    ValueError
        If ``value`` is outside the unsigned 32-bit range.

    Examples
    --------
    >>> int_to_ipv4(0)
    '0.0.0.0'
    >>> int_to_ipv4(4294967295)
    '255.255.255.255'
    >>> int_to_ipv4(3232235777)
    '192.168.1.1'
    """
    if not isinstance(value, int):
        raise TypeError("value must be an integer")

    if value < 0 or value > 0xFFFFFFFF:
        raise ValueError(f"value out of range for 32-bit unsigned integer: {value}")

    octets = [
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF,
    ]
    return ".".join(str(octet) for octet in octets)
