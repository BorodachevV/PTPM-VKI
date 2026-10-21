import unittest
from calculator import TriangleCalculator


class TestTriangleCalculatorSmoke(unittest.TestCase):
    """Smoke-тест класса-обёртки (не дублирует ЛР №2)."""

    def test_returns_tuple_of_two_elements(self):
        result = TriangleCalculator().calculate("3", "4", "5")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()