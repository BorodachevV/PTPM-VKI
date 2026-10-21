import logging

from calculator import TriangleCalculator
from database import TriangleDatabase
from user_interface import UserInterface
from external_service import ExternalService

logger = logging.getLogger(__name__)


class Controller:
    """e. Контроллер — сквозной сценарий бизнес-логики."""

    def __init__(
        self,
        calc: TriangleCalculator,
        db: TriangleDatabase,
        ui: UserInterface,
        external: ExternalService,
    ):
        self.calc = calc
        self.db = db
        self.ui = ui
        self.external = external

    def process(self) -> str:
        parts = self.ui.get_triangle_sides()
        if parts is None or len(parts) != 3:
            return "Ошибка: нужно ввести ровно три значения"

        a, b, c = parts
        cached = self.db.get(a, b, c)

        if cached is not None:
            kind, error = cached
            if kind in ("", "не треугольник"):
                result = f"Результат (из БД): {error}"
            else:
                result = f"Результат (из БД): треугольник {kind}"
        else:
            kind, coords = self.calc.calculate(a, b, c)
            if kind == "":
                error = "введены нечисловые данные"
                result = f"Результат: {error}"
            elif kind == "не треугольник":
                error = "не треугольник"
                result = "Результат: не треугольник"
            else:
                error = ""
                result = f"Результат: треугольник {kind}, вершины {coords}"
            self.db.add(a, b, c, kind, error)

        self.external.send_result(result)
        return result