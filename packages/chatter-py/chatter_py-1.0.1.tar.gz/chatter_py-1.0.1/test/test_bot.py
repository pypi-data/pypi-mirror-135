import unittest
from unittest.mock import Mock, call

from chatter_py import Feature
from chatter_py.bot import Bot, Room
from chatter_py.message import Message, FeatureMessage


class TestBot(unittest.TestCase):

    def test_starting_bot_starts_chat_client_listening(self):
        # given
        chat_client = Mock()

        # when
        bot = Bot(chat_client, Mock())
        bot.start()

        # then
        chat_client.start_listening.assert_called_once()

    def test_room_is_created_for_each_chat_client_room(self):
        # given
        chat_client = Mock()
        bot = Bot(chat_client, [Mock(Feature)], config=None)

        # when
        chat_client.send_to_bot(Message(text=["hello"], room="foo"))
        chat_client.send_to_bot(Message(text=["hello"], room="bar"))

        # then
        self.assertEqual(2, len(bot.rooms))
        self.assertEqual(bot.rooms.keys(), {"foo", "bar"})

    def test_bot_instantiates_rooms_correctly(self):
        # given
        chat_client = Mock()
        room_type = Mock()
        feature_type = Mock()
        config = Mock()
        Bot(chat_client, [feature_type], config, room_type)

        # when
        chat_client.send_to_bot(Message(text=["hello"], room="foo"))

        # then
        room_type.assert_called_once_with([feature_type],
                                          chat_client.send_to_client,
                                          "foo", config)

    def test_message_is_routed_to_correct_room(self):
        # given
        chat_client = Mock()
        room_type = Mock()
        room_foo = Mock()
        room_bar = Mock()
        room_type.side_effect = [room_foo, room_bar]
        Bot(chat_client, [Mock(Feature)], config=None, room_class=room_type)
        foo_message1 = Message(text=["hello"], room="foo")
        bar_message1 = Message(text=["hello"], room="bar")
        foo_message2 = Message(text=["goodbye"], room="foo")

        # when
        chat_client.send_to_bot(foo_message1)
        chat_client.send_to_bot(bar_message1)
        chat_client.send_to_bot(foo_message2)

        # then
        room_foo.send_to_feature.assert_has_calls([call(foo_message1), call(foo_message2)])
        room_bar.send_to_feature.assert_has_calls([call(bar_message1)])


class Stub(Feature):
    def handle(self, message: Message):
        self.send_to_chat(FeatureMessage(text=message.original_text))


class TestRoom(unittest.TestCase):

    def test_room_is_added_to_feature_messages_to_chat_if_room_is_not_present(self):
        # given
        feature = Stub
        send_to_chat = Mock()
        room = Room([feature], send_to_chat, "1")

        # when
        room.features["STUB"].send_to_chat(FeatureMessage(text=["hello"]))

        # then
        send_to_chat.assert_called_once_with(Message(text=["hello"], room="1"))

    def test_data_is_copied_over_from_feature_messages_to_chat(self):
        # given
        feature = Stub
        send_to_chat = Mock()
        room = Room([feature], send_to_chat, "1")

        # when
        room.features["STUB"].send_to_chat(FeatureMessage(text=["hello"], data={"foo": "bar"}))

        # then
        send_to_chat.assert_called_once_with(Message(text=["hello"], room="1",
                                                     data={"foo": "bar"}))

    def test_room_does_not_overwrite_room_on_messages_where_it_is_present(self):
        # given
        feature = Stub
        send_to_chat = Mock()
        room = Room([feature], send_to_chat, "1")

        # when
        room.features["STUB"].send_to_chat(FeatureMessage(text=["hello"], room="bla"))

        # then
        send_to_chat.assert_called_once_with(Message(text=["hello"], room="bla"))

    def test_room_routes_message_to_correct_feature_based_on_text(self):
        # given
        feature = Mock()
        instantiated_feature_a = Mock()
        instantiated_feature_a.name = "foo"
        instantiated_feature_b = Mock()
        instantiated_feature_b.name = "bar"
        feature.side_effect = [instantiated_feature_a, instantiated_feature_b]
        room = Room([feature, feature], print, "1")

        # when
        room.send_to_feature(Message(text=["foo"], room="1"))
        room.send_to_feature(Message(text=["foo", "bla"], room="1"))

        # then
        instantiated_feature_a.handle.assert_has_calls([call(Message(text=[], room="1")),
                                                        call(Message(text=["bla"], room="1"))])
        instantiated_feature_b.handle.assert_not_called()

    def test_room_routes_message_to_correct_feature_irrespective_of_capitalisation(self):
        # given
        feature = Mock()
        instantiated_feature = Mock()
        instantiated_feature.name = "foo"
        feature.return_value = instantiated_feature
        room = Room([feature], print, "1")

        # when
        room.send_to_feature(Message(text=["foo"], room="1"))
        room.send_to_feature(Message(text=["FOO", "bar"], room="1"))
        room.send_to_feature(Message(text=["Foo", "baz"], room="1"))
        room.send_to_feature(Message(text=["foO", "bla"], room="1"))

        # then
        instantiated_feature.handle.assert_has_calls([call(Message(text=[], room="1")),
                                                      call(Message(text=["bar"], room="1")),
                                                      call(Message(text=["baz"], room="1")),
                                                      call(Message(text=["bla"], room="1"))])

    def test_room_does_not_route_to_any_feature_if_command_is_not_recognised(self):
        # given
        feature = Mock()
        instantiated_feature = Mock()
        instantiated_feature.name = "foo"
        feature.return_value = instantiated_feature
        mock_send_to_chat = Mock()
        room = Room([feature], mock_send_to_chat, "1")

        # when
        room.send_to_feature(Message(text=["bar", "baz"], room="1"))

        # then
        mock_send_to_chat.assert_not_called()
        instantiated_feature.handle.assert_not_called()
