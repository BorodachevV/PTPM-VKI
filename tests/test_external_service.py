import unittest
from external_service import MockEmailService


class TestMockEmailService(unittest.TestCase):
    def test_send_returns_true(self):
        self.assertTrue(MockEmailService().send_result("hi"))

    def test_send_records_messages(self):
        service = MockEmailService()
        service.send_result("one")
        service.send_result("two")
        self.assertEqual(service.sent_messages, ["one", "two"])


if __name__ == "__main__":
    unittest.main()