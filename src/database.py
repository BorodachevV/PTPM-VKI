"""Модуль работы с базой данных SQLite."""
import sqlite3
from typing import Optional, List, Dict, Any


class DatabaseRepository:
    """Репозиторий для работы с таблицей comments."""

    MAX_NAME_LENGTH = 256
    MAX_MESSAGE_LENGTH = 8096

    def __init__(self, db_path: str):
        """
        :param db_path: путь к файлу БД или ':memory:' для тестов.
        """
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    # ------------------------------------------------------------------ #
    #                              DDL                                   #
    # ------------------------------------------------------------------ #
    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id      INTEGER PRIMARY KEY,
                name    TEXT NOT NULL,
                message TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    # ------------------------------------------------------------------ #
    #                          Валидаторы                                #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _validate_id(comment_id: int) -> None:
        # bool — подкласс int, поэтому проверяем явно
        if not isinstance(comment_id, int) or isinstance(comment_id, bool):
            raise TypeError(f"ID должен быть int, получено {type(comment_id).__name__}")

    @classmethod
    def _validate_name(cls, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(f"name должен быть str, получено {type(name).__name__}")
        if not name:
            raise ValueError("name не может быть пустым")
        if len(name) > cls.MAX_NAME_LENGTH:
            raise ValueError(
                f"name длиннее {cls.MAX_NAME_LENGTH} символов (было {len(name)})"
            )

    @classmethod
    def _validate_message(cls, message: str) -> None:
        if not isinstance(message, str):
            raise TypeError(f"message должен быть str, получено {type(message).__name__}")
        if not message:
            raise ValueError("message не может быть пустым")
        if len(message) > cls.MAX_MESSAGE_LENGTH:
            raise ValueError(
                f"message длиннее {cls.MAX_MESSAGE_LENGTH} символов (было {len(message)})"
            )

    # ------------------------------------------------------------------ #
    #                          CRUD-методы                               #
    # ------------------------------------------------------------------ #
    def add(self, comment_id: int, username: str, message: str) -> bool:
        """Добавление новой записи. Возвращает True при успехе."""
        self._validate_id(comment_id)
        self._validate_name(username)
        self._validate_message(message)
        try:
            self._conn.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message),
            )
            self._conn.commit()
            return True
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"Запись с ID={comment_id} уже существует (нарушение PRIMARY KEY)"
            ) from exc

    def get_by_id(self, comment_id: int) -> Optional[Dict[str, Any]]:
        """Возвращает одну запись как dict или None, если её нет."""
        self._validate_id(comment_id)
        cur = self._conn.execute(
            "SELECT id, name, message FROM comments WHERE id = ?",
            (comment_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def get_by_name(self, username: str) -> List[Dict[str, Any]]:
        """Возвращает список всех записей, оставленных пользователем."""
        if not isinstance(username, str):
            raise TypeError("username должен быть str")
        cur = self._conn.execute(
            "SELECT id, name, message FROM comments WHERE name = ? ORDER BY id",
            (username,),
        )
        return [dict(row) for row in cur.fetchall()]

    def update(self, comment_id: int, new_message: str) -> bool:
        """Изменение сообщения по ID. Возвращает True или бросает исключение."""
        self._validate_id(comment_id)
        self._validate_message(new_message)
        cur = self._conn.execute(
            "UPDATE comments SET message = ? WHERE id = ?",
            (new_message, comment_id),
        )
        self._conn.commit()
        if cur.rowcount == 0:
            raise ValueError(f"Запись с ID={comment_id} не найдена — обновление невозможно")
        return True

    def delete(self, comment_id: int) -> bool:
        """Удаление строки по ID. Возвращает True, если запись была удалена."""
        self._validate_id(comment_id)
        cur = self._conn.execute(
            "DELETE FROM comments WHERE id = ?",
            (comment_id,),
        )
        self._conn.commit()
        return cur.rowcount > 0

    # ------------------------------------------------------------------ #
    #                          Служебные методы                          #
    # ------------------------------------------------------------------ #
    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "DatabaseRepository":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()