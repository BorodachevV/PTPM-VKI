from abc import ABC, abstractmethod
from typing import Tuple, Optional


class UserInterface(ABC):
    """c. Интерфейс взаимодействия с пользователем."""

    @abstractmethod
    def get_triangle_sides(self) -> Optional[Tuple[str, str, str]]:
        ...


class ConsoleUserInterface(UserInterface):
    def get_triangle_sides(self):
        raw = input("Введите стороны A B C (Ctrl+C для выхода): ").strip()
        return tuple(raw.split())