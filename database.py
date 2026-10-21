import sqlite3


class TriangleDatabase:
    """b. Класс работы с БД SQLite."""

    def __init__(self, db_path: str = ":memory:"):
        self._conn = sqlite3.connect(db_path)
        self._init_db() 

    def _init_db(self) -> None:
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side1 TEXT NOT NULL,
                side2 TEXT NOT NULL,
                side3 TEXT NOT NULL,
                triangle_type TEXT NOT NULL,
                error_message TEXT NOT NULL DEFAULT '',
                PRIMARY KEY (side1, side2, side3)
            )
        """)
        self._conn.commit()

    def add(self, side1, side2, side3, triangle_type, error_message=""):
        self._conn.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (side1, side2, side3, triangle_type, error_message),
        )
        self._conn.commit()

    def get(self, side1, side2, side3):
        cur = self._conn.execute(
            "SELECT triangle_type, error_message FROM triangles "
            "WHERE side1=? AND side2=? AND side3=?",
            (side1, side2, side3),
        )
        return cur.fetchone()

    def delete(self, side1, side2, side3) -> int:
        cur = self._conn.execute(
            "DELETE FROM triangles WHERE side1=? AND side2=? AND side3=?",
            (side1, side2, side3),
        )
        self._conn.commit()
        return cur.rowcount

    def close(self) -> None:
        self._conn.close()