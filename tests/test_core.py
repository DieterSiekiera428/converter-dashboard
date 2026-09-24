"""Tests for ipv4_int_converter.core."""

import unittest

from ipv4_int_converter import int_to_ipv4, ipv4_to_int


class TestIPv4ToInt(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(ipv4_to_int("0.0.0.0"), 0)

    def test_maximum(self):
        self.assertEqual(ipv4_to_int("255.255.255.255"), 0xFFFFFFFF)

    def test_common_address(self):
        self.assertEqual(ipv4_to_int("192.168.1.1"), 3232235777)

    def test_single_digit_octets(self):
        self.assertEqual(ipv4_to_int("1.2.3.4"), 0x01020304)

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            ipv4_to_int(123)

    def test_leading_zero_rejected(self):
        # Leading zeros are explicitly disallowed to avoid octal ambiguity.
        with self.assertRaises(ValueError):
            ipv4_to_int("192.168.001.001")

    def test_out_of_range_octet_rejected(self):
        with self.assertRaises(ValueError):
            ipv4_to_int("256.0.0.0")

    def test_missing_octet_rejected(self):
        with self.assertRaises(ValueError):
            ipv4_to_int("192.168.1")

    def test_extra_octet_rejected(self):
        with self.assertRaises(ValueError):
            ipv4_to_int("192.168.1.1.1")

    def test_empty_string_rejected(self):
        with self.assertRaises(ValueError):
            ipv4_to_int("")

    def test_non_numeric_octet_rejected(self):
        with self.assertRaises(ValueError):
            ipv4_to_int("192.168.1.a")

    def test_negative_octet_rejected(self):
        with self.assertRaises(ValueError):
            ipv4_to_int("192.168.-1.1")


class TestIntToIPv4(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(int_to_ipv4(0), "0.0.0.0")

    def test_maximum(self):
        self.assertEqual(int_to_ipv4(0xFFFFFFFF), "255.255.255.255")

    def test_common_address(self):
        self.assertEqual(int_to_ipv4(3232235777), "192.168.1.1")

    def test_single_digit_octets(self):
        self.assertEqual(int_to_ipv4(0x01020304), "1.2.3.4")

    def test_non_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            int_to_ipv4("123")

    def test_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            int_to_ipv4(-1)

    def test_too_large_raises_value_error(self):
        with self.assertRaises(ValueError):
            int_to_ipv4(0x100000000)

    def test_bool_accepted_as_integer(self):
        # bool is a subclass of int; we accept it for consistency with
        # Python's numeric model.
        self.assertEqual(int_to_ipv4(True), "0.0.0.1")
        self.assertEqual(int_to_ipv4(False), "0.0.0.0")


class TestRoundTrip(unittest.TestCase):
    def test_round_trip_representative_addresses(self):
        addresses = [
            "0.0.0.0",
            "0.0.0.1",
            "1.2.3.4",
            "10.0.0.255",
            "127.0.0.1",
            "172.16.254.1",
            "192.168.1.1",
            "255.255.255.254",
            "255.255.255.255",
        ]
        for address in addresses:
            with self.subTest(address=address):
                self.assertEqual(int_to_ipv4(ipv4_to_int(address)), address)

    def test_round_trip_all_boundary_values(self):
        boundary_integers = [0, 1, 2, 254, 255, 256, 257, 65535, 65536,
                             16777215, 16777216, 4294967294, 4294967295]
        for value in boundary_integers:
            with self.subTest(value=value):
                self.assertEqual(ipv4_to_int(int_to_ipv4(value)), value)


if __name__ == "__main__":
    unittest.main()
