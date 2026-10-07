import math
import os
import sys
import unittest

# Чтобы unittest видел my_project.py из src
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from my_project import calculate_triangle


class TestCalculateTriangle(unittest.TestCase):

    # ------------------------------------------------------------------
    # Классификация треугольника
    # ------------------------------------------------------------------

    def test_ravnostoronniy_triangle_detected(self):
        """Равносторонний треугольник определяется корректно."""
        kind, coords = calculate_triangle("10", "10", "10")
        self.assertEqual(kind, "равносторонний")
        self.assertEqual(len(coords), 3)

    def test_ravnobedrenniy_triangle_detected(self):
        """Равнобедренный треугольник определяется корректно."""
        kind, _ = calculate_triangle("5", "5", "8")
        self.assertEqual(kind, "равнобедренный")

    def test_raznostoronniy_triangle_detected(self):
        """Разносторонний треугольник определяется корректно."""
        kind, _ = calculate_triangle("3", "4", "5")
        self.assertEqual(kind, "разносторонний")

    def test_ravnobedrenniy_detected_by_second_pair(self):
        """Равнобедренность определяется и по другой паре равных сторон (a == c)."""
        kind, _ = calculate_triangle("7", "5", "7")
        self.assertEqual(kind, "равнобедренный")

    # ------------------------------------------------------------------
    # Отрицательные сценарии: некорректные стороны
    # ------------------------------------------------------------------

    def test_triangle_inequality_violation_returns_not_triangle(self):
        """Нарушение неравенства треугольника: 1 + 2 < 10."""
        kind, coords = calculate_triangle("1", "2", "10")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_degenerate_triangle_is_not_triangle(self):
        """Вырожденный треугольник (a + b == c) не считается треугольником."""
        kind, coords = calculate_triangle("2", "3", "5")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_negative_side_returns_not_triangle(self):
        """Отрицательная сторона: не треугольник, код (-1, -1)."""
        kind, coords = calculate_triangle("-5", "3", "4")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_zero_side_returns_not_triangle(self):
        """Нулевая сторона: не треугольник."""
        kind, coords = calculate_triangle("0", "3", "4")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    def test_non_numeric_input_returns_code_minus_2(self):
        """Нечисловые данные: пустой вид и код (-2, -2)."""
        kind, coords = calculate_triangle("abc", "3", "4")
        self.assertEqual(kind, "")
        self.assertEqual(coords, [(-2, -2)] * 3)

    def test_infinity_input_returns_not_triangle(self):
        """Бесконечность (inf) не является допустимой стороной."""
        kind, coords = calculate_triangle("inf", "3", "4")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(coords, [(-1, -1)] * 3)

    


if __name__ == "__main__":
    unittest.main()