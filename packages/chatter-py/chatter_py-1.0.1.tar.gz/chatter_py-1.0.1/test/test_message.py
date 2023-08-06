import unittest

from chatter_py import Message


class TestMessage(unittest.TestCase):

    def test_message_original_text_is_set_to_message_text_on_init(self):
        # when
        m = Message(text=["hello", "and", "welcome"], room="1")

        # then
        self.assertEqual(m.original_text, m.text)
