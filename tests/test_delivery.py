import os
import sys
import unittest

# Чтобы unittest видел модули из src при запуске из PyCharm/терминала
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from delivery_service import calculate_delivery_cost

SEND_DATE = "2026-09-03"
ERROR = (-1, "0000-00-00")


class TestDeliveryCost(unittest.TestCase):

    # ------------------------------------------------------------------
    # Базовый тариф
    # ------------------------------------------------------------------

    def test_base_cost_minimal_order(self):
        """Минимальный заказ: вес 0.1 кг, 1 км, обычный -> 200 + 1*5 = 205 руб."""
        cost, date = calculate_delivery_cost(0.1, 1, "обычный")
        self.assertEqual(cost, 205)
        self.assertEqual(date, "2026-09-04")

    def test_base_cost_max_distance(self):
        """Максимальная дистанция 5000 км: 200 + 25000 = 25200 руб., 10 дней."""
        cost, date = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertEqual(cost, 25200)
        self.assertEqual(date, "2026-09-13")

    def test_delivery_date_for_mid_distance(self):
        """Дистанция 1500 км -> 3 дня в пути -> дата 2026-09-06."""
        _, date = calculate_delivery_cost(1.0, 1500, "обычный")
        self.assertEqual(date, "2026-09-06")

    # ------------------------------------------------------------------
    # Проверка входных данных
    # ------------------------------------------------------------------

    def test_weight_below_minimum_rejected(self):
        """Вес меньше 0.1 кг отклоняется."""
        self.assertEqual(
            calculate_delivery_cost(0.09, 100, "обычный"),
            ERROR
        )

    def test_weight_above_maximum_rejected(self):
        """Вес больше 50 кг отклоняется."""
        self.assertEqual(
            calculate_delivery_cost(50.1, 100, "обычный"),
            ERROR
        )

    def test_distance_below_minimum_rejected(self):
        """Дистанция меньше 1 км отклоняется."""
        self.assertEqual(
            calculate_delivery_cost(1.0, 0, "обычный"),
            ERROR
        )

    def test_distance_above_maximum_rejected(self):
        """Дистанция больше 5000 км отклоняется."""
        self.assertEqual(
            calculate_delivery_cost(1.0, 5001, "обычный"),
            ERROR
        )

    def test_invalid_package_type_rejected(self):
        """Неизвестный тип посылки отклоняется."""
        self.assertEqual(
            calculate_delivery_cost(1.0, 100, "перishable"),
            ERROR
        )

    def test_boundary_values_accepted(self):
        """Граничные значения веса и дистанции (0.1/50.0, 1/5000) допустимы."""
        self.assertGreater(
            calculate_delivery_cost(0.1, 1, "обычный")[0],
            0
        )
        self.assertGreater(
            calculate_delivery_cost(50.0, 5000, "обычный")[0],
            0
        )

    # ------------------------------------------------------------------
    # Весовые коэффициенты и надбавки
    # ------------------------------------------------------------------

    def test_weight_coefficient_between_5_and_20_kg(self):
        """Вес 6 кг -> коэффициент 1.2: (200 + 2*5) * 1.2 = 252 руб."""
        cost, _ = calculate_delivery_cost(6.0, 2, "обычный")
        self.assertEqual(cost, 252)

    

if __name__ == "__main__":
    unittest.main()