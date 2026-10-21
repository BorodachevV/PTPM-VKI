import unittest
from database import TriangleDatabase


class TestTriangleDatabase(unittest.TestCase):
    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_get(self):
        self.db.add("3", "4", "5", "разносторонний", "")
        self.assertEqual(self.db.get("3", "4", "5"), ("разносторонний", ""))

    def test_get_missing_returns_none(self):
        self.assertIsNone(self.db.get("1", "2", "3"))

    def test_delete_existing(self):
        self.db.add("3", "4", "5", "разносторонний", "")
        self.assertEqual(self.db.delete("3", "4", "5"), 1)
        self.assertIsNone(self.db.get("3", "4", "5"))

    def test_delete_nonexistent(self):
        self.assertEqual(self.db.delete("1", "2", "3"), 0)

    def test_replace_same_key(self):
        self.db.add("3", "4", "5", "старый", "")
        self.db.add("3", "4", "5", "новый", "err")
        self.assertEqual(self.db.get("3", "4", "5"), ("новый", "err"))


if __name__ == "__main__":
    unittest.main()