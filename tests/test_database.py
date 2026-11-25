"""Тесты для DatabaseRepository."""
import unittest
from src.database import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):

    def setUp(self):
        # Свежая in-memory БД перед каждым тестом
        self.repo = DatabaseRepository(":memory:")

    def tearDown(self):
        self.repo.close()

    # ======================== add ==================================== #
    def test_add_success(self):
        result = self.repo.add(1, "alice", "Hello")
        self.assertTrue(result)
        self.assertEqual(self.repo.get_by_id(1)["message"], "Hello")

    def test_add_duplicate_id_raises(self):
        self.repo.add(1, "alice", "Hello")
        with self.assertRaises(ValueError):
            self.repo.add(1, "bob", "Another")

    def test_add_invalid_message_too_long(self):
        with self.assertRaises(ValueError):
            self.repo.add(1, "alice", "x" * 8097)

    def test_add_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.repo.add(1, 12345, "msg")

    # ======================== get_by_id ============================== #
    def test_get_by_id_exists(self):
        self.repo.add(42, "alice", "hi")
        row = self.repo.get_by_id(42)
        self.assertIsNotNone(row)
        self.assertEqual(row["id"], 42)
        self.assertEqual(row["name"], "alice")
        self.assertEqual(row["message"], "hi")

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.repo.get_by_id(999))

    # ======================== get_by_name ============================ #
    def test_get_by_name_multiple(self):
        self.repo.add(1, "alice", "one")
        self.repo.add(2, "alice", "two")
        self.repo.add(3, "bob", "three")
        rows = self.repo.get_by_name("alice")
        self.assertEqual(len(rows), 2)
        self.assertEqual({r["id"] for r in rows}, {1, 2})

    def test_get_by_name_empty(self):
        self.assertEqual(self.repo.get_by_name("ghost"), [])

    # ======================== update ================================= #
    def test_update_success(self):
        self.repo.add(1, "alice", "old")
        self.assertTrue(self.repo.update(1, "new"))
        self.assertEqual(self.repo.get_by_id(1)["message"], "new")

    def test_update_nonexistent_id_raises(self):
        with self.assertRaises(ValueError):
            self.repo.update(999, "new")

    def test_update_message_too_long_raises(self):
        self.repo.add(1, "alice", "old")
        with self.assertRaises(ValueError):
            self.repo.update(1, "y" * 8097)

    # ======================== delete ================================= #
    def test_delete_success(self):
        self.repo.add(1, "alice", "hi")
        self.assertTrue(self.repo.delete(1))
        self.assertIsNone(self.repo.get_by_id(1))

    def test_delete_nonexistent_returns_false(self):
        self.assertFalse(self.repo.delete(12345))


if __name__ == "__main__":
    unittest.main()