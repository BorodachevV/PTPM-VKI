import math
import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)


class TriangleCalculator:
    """a. Класс вычислений — обёртка над логикой из ЛР №1."""

    def calculate(
        self, a_raw: str, b_raw: str, c_raw: str
    ) -> Tuple[str, List[Tuple[int, int]]]:
        try:
            sides = []
            for raw in (a_raw, b_raw, c_raw):
                value = float(raw)
                if not math.isfinite(value):
                    logger.warning("Не конечное число: %r", raw)
                    return "не треугольник", [(-1, -1)] * 3
                sides.append(value)
            a, b, c = sides

            if a <= 0 or b <= 0 or c <= 0:
                return "не треугольник", [(-1, -1)] * 3

            tol = 1e-9 * max(a, b, c)
            if a + b <= c + tol or a + c <= b + tol or b + c <= a + tol:
                return "не треугольник", [(-1, -1)] * 3

            eps = 1e-9
            if abs(a - b) < eps and abs(b - c) < eps:
                kind = "равносторонний"
            elif abs(a - b) < eps or abs(b - c) < eps or abs(a - c) < eps:
                kind = "равнобедренный"
            else:
                kind = "разносторонний"

            cx = (a * a + c * c - b * b) / (2 * c)
            cy = math.sqrt(max(0.0, a * a - cx * cx))
            max_dim = max(c, cy)
            scale = 100.0 / max_dim if max_dim > 100.0 else 1.0
            coords = [
                (int(round(0 * scale)), int(round(0 * scale))),
                (int(round(c * scale)), int(round(0 * scale))),
                (int(round(cx * scale)), int(round(cy * scale))),
            ]
            return kind, coords
        except ValueError:
            return "", [(-2, -2)] * 3
        except Exception:
            logger.exception("Неожиданная ошибка")
            return "не треугольник", [(-1, -1)] * 3