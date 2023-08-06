import unittest
from unittest.mock import Mock

from chatter_py.feature import subcommand, Feature
from chatter_py.message import Message


class TestSubcommand(unittest.TestCase):

    def test_decorating_a_method_sets_attributes_on_it(self):
        # given
        trigger_attr = subcommand.TRIGGERS

        # when
        @subcommand("foo", "bar")
        def some_method(a, b):
            print("hello")

        # when/then
        assert getattr(some_method, trigger_attr) == ("foo", "bar")

    def test_providing_no_triggers_throws_an_error(self):
        # when/then
        with self.assertRaisesRegex(TypeError, "At least one trigger word must be provided!"):
            subcommand()(Mock())

    def test_decorating_object_does_not_change_it(self):
        # given
        def method(a, b):
            pass

        # when
        method_after_altering = subcommand("foo")(method)

        # then
        self.assertEqual(type(method_after_altering), type(method))

    def test_decorating_a_method_with_incorrect_number_of_args_throws_an_error(self):
        # given
        def method_with_bad_sig():
            pass

        # when/then
        msg = "A method decorated with subcommand must take two arguments.*"
        with self.assertRaisesRegex(TypeError, msg):
            subcommand("foo")(method_with_bad_sig)


class Foo(Feature):

    @subcommand("echo")
    def a(self, message: Message):
        self.send_to_chat(message)

    @subcommand("baz", "bla")
    def b(self, message: Message):
        pass


class TestFeature(unittest.TestCase):

    def test_feature_passes_a_message_to_the_correct_subcommand(self):
        # given
        send_to_chat = Mock()
        message = Message(text=["echo", "bla"], room="1")
        f = Foo(send_to_chat)

        # when
        f.handle(message)

        # then
        send_to_chat.assert_called_once_with(Message(text=["bla"], room="1"))

    def test_feature_ignores_a_message_that_does_not_match_a_subcommand(self):
        # given
        send_to_chat = Mock()
        message = Message(text=["bad", "command"], room="1")
        f = Foo(send_to_chat)

        # when
        f.handle(message)

        # then
        send_to_chat.assert_not_called()
