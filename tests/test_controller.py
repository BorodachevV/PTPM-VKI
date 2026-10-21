import unittest
from unittest.mock import Mock, patch

from calculator import TriangleCalculator
from database import TriangleDatabase
from external_service import ExternalService
from user_interface import UserInterface
from controller import Controller


class TestControllerIntegration(unittest.TestCase):
    """Интеграционные тесты Controller с реальной БД и заглушками UI/External."""

    def setUp(self):
        self.calc = TriangleCalculator()
        self.db = TriangleDatabase(":memory:")
        self.ui = Mock(spec=UserInterface)              # заглушка ввода
        self.external = Mock(spec=ExternalService)      # заглушка внешнего сервиса
        self.external.send_result.return_value = True
        self.controller = Controller(self.calc, self.db, self.ui, self.external)

    def tearDown(self):
        self.db.close()

    def test_new_triangle_computed_stored_and_sent(self):
        """Валидный треугольник: вычисляется, пишется в БД, отправляется наружу."""
        self.ui.get_triangle_sides.return_value = ("3", "4", "5")
        result = self.controller.process()

        self.assertIn("разносторонний", result)
        self.assertEqual(self.db.get("3", "4", "5"), ("разносторонний", ""))
        self.external.send_result.assert_called_once()

    def test_second_call_reads_from_cache_without_calc(self):
        """Второй вызов того же ввода берёт результат из БД (калькулятор не вызывается)."""
        self.ui.get_triangle_sides.return_value = ("10", "10", "10")
        self.controller.process()

        with patch.object(self.calc, "calculate") as mock_calc:
            result = self.controller.process()
            mock_calc.assert_not_called()
        self.assertIn("БД", result)

    def test_invalid_argument_count(self):
        """Неверное количество аргументов — ошибка, БД и внешний сервис не задействованы."""
        self.ui.get_triangle_sides.return_value = ("3", "4")
        result = self.controller.process()
        self.assertIn("Ошибка", result)
        self.external.send_result.assert_not_called()

    def test_non_numeric_input(self):
        """Нечисловые данные сохраняются в БД с пустым типом и текстом ошибки."""
        self.ui.get_triangle_sides.return_value = ("abc", "3", "4")
        result = self.controller.process()

        self.assertIn("нечисловые", result)
        self.assertEqual(self.db.get("abc", "3", "4"),
                         ("", "введены нечисловые данные"))
        self.external.send_result.assert_called_once()

    def test_not_a_triangle_stored(self):
        """Нарушение неравенства треугольника фиксируется в БД."""
        self.ui.get_triangle_sides.return_value = ("1", "2", "10")
        result = self.controller.process()

        self.assertIn("не треугольник", result)
        self.assertEqual(self.db.get("1", "2", "10"),
                         ("не треугольник", "не треугольник"))

    def test_external_service_receives_result_string(self):
        """Проверка, что во внешний сервис уходит строка-результат."""
        self.ui.get_triangle_sides.return_value = ("10", "10", "10")
        self.controller.process()

        self.external.send_result.assert_called_once()
        msg = self.external.send_result.call_args[0][0]
        self.assertIn("равносторонний", msg)

    def test_ui_returns_none(self):
        """Если UI вернул None — корректно возвращаем сообщение об ошибке."""
        self.ui.get_triangle_sides.return_value = None
        result = self.controller.process()
        self.assertIn("Ошибка", result)
        self.external.send_result.assert_not_called()


if __name__ == "__main__":
    unittest.main()