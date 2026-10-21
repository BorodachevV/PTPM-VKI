from abc import ABC, abstractmethod


class ExternalService(ABC):
    """d. Интерфейс сторонней зависимости (email-сервер и т.п.)."""

    @abstractmethod
    def send_result(self, message: str) -> bool:
        ...


class MockEmailService(ExternalService):
    """Имитация отправки на внешний сервер."""

    def __init__(self):
        self.sent_messages: list[str] = []

    def send_result(self, message: str) -> bool:
        self.sent_messages.append(message)
        print(f"[EMAIL] {message}")
        return True