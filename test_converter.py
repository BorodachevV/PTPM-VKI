import unittest

from converter import Converter


class TestConverter(unittest.TestCase):
    def test_upper_range_returns_1000(self):
        cases = [100.7, 100.8, 101.0, 1000.0]
        for x in cases:
            with self.subTest(x=x):
                self.assertEqual(Converter.do(x), 1000)

    def test_positive_range_truncates_to_int(self):
        cases = [
            (0.1, 0),
            (0.9, 0),
            (1.0, 1),
            (65.7, 65),
            (99.9, 99),
            (100.6, 100),
        ]
        for x, expected in cases:
            with self.subTest(x=x):
                self.assertEqual(Converter.do(x), expected)

    def test_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

        with self.assertRaises(ValueError):
            Converter.do(-0.0)

    def test_negative_range_to_zero(self):
        cases = [
            (-0.1, -5),
            (-0.9, -5),
            (-1.0, -6),
            (-15.5, -20),
            (-30.3, -35),
            (-30.4, -35),
        ]
        for x, expected in cases:
            with self.subTest(x=x):
                self.assertEqual(Converter.do(x), expected)

    def test_far_negative_range_returns_minus_2000(self):
        cases = [-30.5, -30.6, -94.5, -2000.0]
        for x in cases:
            with self.subTest(x=x):
                self.assertEqual(Converter.do(x), -2000)

    def test_boundary_values(self):
        self.assertEqual(Converter.do(100.7), 1000)
        self.assertEqual(Converter.do(100.6), 100)
        self.assertEqual(Converter.do(0.1), 0)
        self.assertEqual(Converter.do(-0.1), -5)
        self.assertEqual(Converter.do(-30.4), -35)
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_return_type_is_int(self):
        for x in [100.7, 65.7, -0.1, -30.5]:
            with self.subTest(x=x):
                self.assertIsInstance(Converter.do(x), int)


if __name__ == "__main__":
    unittest.main()