import unittest

from app import greeting


class GreetingTest(unittest.TestCase):
    def test_default(self):
        self.assertEqual(greeting(""), {"message": "hello, world"})

    def test_name_is_trimmed_and_capped(self):
        self.assertEqual(len(greeting("x" * 500)["message"]), len("hello, ") + 64)


if __name__ == "__main__":
    unittest.main()
