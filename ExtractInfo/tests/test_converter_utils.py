import unittest
from ExtractInfo.converter_utils import (
    StringConverter,
    FloatConverter,
    WebsiteConverter,
    EmailConverter,
    PhoneConverter,
    IntConverter,
)


class TestStringConverter(unittest.TestCase):
    def test_strip_whitespace(self):
        converter = StringConverter("  hello world  ")
        self.assertEqual(converter.convert(), "hello world")

    def test_empty_string(self):
        converter = StringConverter("")
        self.assertEqual(converter.convert(), "")

    def test_no_whitespace(self):
        converter = StringConverter("test")
        self.assertEqual(converter.convert(), "test")

    def test_only_whitespace(self):
        converter = StringConverter("   ")
        self.assertEqual(converter.convert(), "")

    def test_non_string_value(self):
        with self.assertRaises(AttributeError):
            converter = StringConverter(123)
            converter.convert()

    def test_phone_converter(self):
        converter = PhoneConverter("123-456-7890")
        self.assertEqual(converter.convert(), "+1 123-456-7890")

        converter = PhoneConverter("+ 11  (123) 456-7890  ")
        self.assertEqual(converter.convert(), "+11 123-456-7890")

        converter = PhoneConverter("(480) 963-4561")
        self.assertEqual(converter.convert(), "+1 480-963-4561")

    def test_email_converter(self):
        converter = EmailConverter("hdf@fjgjhg.")
        with self.assertRaises(ValueError):
            converter.convert()

        converter = EmailConverter("   hdf@fjgjhg.co.in   ")
        self.assertEqual(converter.convert(), "hdf@fjgjhg.co.in")

    def test_website_converter(self):
        converter = WebsiteConverter("https://example.com")
        self.assertEqual(converter.convert(), "https://example.com")

        converter = WebsiteConverter("   http://example.com/path   ")
        self.assertEqual(converter.convert(), "http://example.com/path")

        converter = WebsiteConverter("invalid-url")
        with self.assertRaises(ValueError):
            converter.convert()

    def float_values(self):
        converter = FloatConverter("  123.456  ")
        self.assertEqual(converter.convert(), 123.456)

        converter = FloatConverter("   -78.9   ")
        self.assertEqual(converter.convert(), -78.9)

        converter = FloatConverter("0.001")
        self.assertEqual(converter.convert(), 0.001)

        with self.assertRaises(ValueError):
            converter = FloatConverter("invalid")
            converter.convert()

    def test_int_converter(self):
        converter = IntConverter("  123  ")
        self.assertEqual(converter.convert(), 123)

        converter = IntConverter("   -456   ")
        self.assertEqual(converter.convert(), -456)

        converter = IntConverter(123)
        self.assertEqual(converter.convert(), 123)

        converter = IntConverter(-456)
        self.assertEqual(converter.convert(), -456)

        converter = IntConverter("0")
        self.assertEqual(converter.convert(), 0)

        with self.assertRaises(ValueError):
            converter = IntConverter("invalid")
            converter.convert()


if __name__ == "__main__":
    unittest.main()
