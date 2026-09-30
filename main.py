import logging
import sys
import os


log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),                     # в консоль
        logging.FileHandler("logs/file_txt.log", encoding="utf-8"),  # в файл
    ],
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")

import re
import hashlib
import math
import traceback
from typing import Optional, Tuple, List





def calculate_triangle(a_raw: str, b_raw: str, c_raw: str) -> Tuple[str, List[Tuple[int, int]]]:
    """
    Определяет вид треугольника по трём сторонам и возвращает координаты
    вершин для отрисовки в поле 100x100 px.

    Возвращает: (тип, [(x1,y1), (x2,y2), (x3,y3)])
      - равносторонний / равнобедренный / разносторонний
      - "" (пустая строка) + координаты (-2, -2) — нечисловые входные данные
      - "не треугольник" + координаты (-1, -1) — числа некорректны
    """
    try:
        sides = []
        for raw in (a_raw, b_raw, c_raw):
            value = float(raw)
            if not math.isfinite(value):
                logging.error(f"Некорректное число (не конечное): '{raw}'")
                return "не треугольник", [(-1, -1)] * 3
            sides.append(value)
        a, b, c = sides
        logging.debug(f"Стороны успешно распознаны: a={a}, b={b}, c={c}")

        if a <= 0 or b <= 0 or c <= 0:
            logging.warning("Сторона не является положительным числом")
            return "не треугольник", [(-1, -1)] * 3

        # Неравенство треугольника
        if a + b <= c or a + c <= b or b + c <= a:
            logging.warning(f"Нарушено неравенство треугольника: {a}, {b}, {c}")
            return "не треугольник", [(-1, -1)] * 3

        eps = 1e-9
        if abs(a - b) < eps and abs(b - c) < eps:
            kind = "равносторонний"
        elif abs(a - b) < eps or abs(b - c) < eps or abs(a - c) < eps:
            kind = "равнобедренный"
        else:
            kind = "разносторонний"
        logging.debug(f"Определён вид треугольника: {kind}")

        # Геометрия: A=(0,0), B=(c,0), C — по теореме косинусов
        cx = (a * a + c * c - b * b) / (2 * c)
        cy = math.sqrt(max(0.0, a * a - cx * cx))

        # Масштабирование под поле 100x100 px с сохранением пропорций
        max_dim = max(c, cy)
        scale = 100.0 / max_dim if max_dim > 100.0 else 1.0
        coords = [(int(round(0 * scale)), int(round(0 * scale))),
                  (int(round(c * scale)), int(round(0 * scale))),
                  (int(round(cx * scale)), int(round(cy * scale)))]
        logging.debug(f"Координаты вершин (масштаб {scale:.4f}): {coords}")

        return kind, coords

    except ValueError:
        # Нечисловые данные
        logging.error("Входные данные не являются вещественными числами")
        return "", [(-2, -2)] * 3
    except Exception:
        logging.error("Непредвиденная ошибка при вычислении треугольника")
        logging.exception("Traceback:")
        return "не треугольник", [(-1, -1)] * 3

def demo_variant_1() -> None:
    logging.info("=== Демонстрация Варианта 1: треугольник ===")
    test_cases = [
        ("10", "10", "10"),      # равносторонний
        ("5", "5", "8"),         # равнобедренный
        ("3", "4", "5"),         # разносторонний
        ("1", "2", "10"),        # не треугольник
        ("-5", "3", "4"),        # не треугольник (отрицательная сторона)
        ("abc", "3", "4"),       # нечисловые данные
    ]
    for a, b, c in test_cases:
        logging.info(f"Запрос: A={a!r}, B={b!r}, C={c!r}")
        kind, coords = calculate_triangle(a, b, c)
        logging.info(f"Результат: тип='{kind}', координаты={coords}")

if __name__ == "__main__":
    demo_variant_1()
    print()
    logging.info("Приложение завершено")