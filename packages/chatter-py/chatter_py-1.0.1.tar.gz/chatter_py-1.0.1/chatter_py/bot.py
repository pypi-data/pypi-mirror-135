from typing import Dict, Type, Iterable, Callable, Union

from chatter_py.chat_client import ChatClient
from chatter_py.feature import Feature
from chatter_py.message import Message, FeatureMessage


class Room:
    """A :class:`Room` is composed of :class:`~chatter_py.feature.Feature` classes,
    and handles routing a :class:`~chatter_py.message.Message` to the correct
    :class:`Feature` based on what is contained within the :class:`Message`.

    The default :class:`Room` implementation used by the :class:`Bot` routes
    a :class:`~chatter_py.message.Message` based on the first word of its text. If
    the first word in the text matches a :class:`~chatter_py.feature.Feature`'s
    name, the first word of the text will be removed and the message will be
    passed to the Feature to handle.

    For custom behaviour, :class:`Room` can be subclassed and
    :func:`send_to_feature` overridden. The new Room type can be passed to the
    Bot to be used instead.

    :param feature_types: The Feature classes to enable for each room
    :param send_to_chat: A callable to be used by features to send messages to
        the chat client
    :param address: The unique address of the room
    :param config: Config that can be accessed by the Features

    """

    def __init__(self, feature_types: Iterable[Type[Feature]],
                 send_to_chat: Callable[[Message], None],
                 address: str, config=None):
        self.address = address
        self._send_to_chat = send_to_chat
        self.features: Dict[str, Feature] = {}

        for feature_type in feature_types:
            feature = feature_type(self._enriched_send_to_chat, config)
            self.features[feature.name.upper()] = feature

    def send_to_feature(self, message: Message) -> None:
        """
        Route a :class:`~chatter_py.message.Message` to a
        :class:`~chatter_py.feature.Feature`. The default :class:`Room` behaviour
        is to route a :class:`~chatter_py.message.Message` based on the first word
        of its text. However, :class:`Bot` will accept a subclass of
        :class:`Room` if some other behaviour is desired.

        :param message: the :class:`~chatter_py.message.Message` to pass to a
            :class:`~chatter_py.feature.Feature`
        """
        if message.text[0].upper() in self.features:
            feature = message.text.pop(0).upper()
            self.features[feature].handle(message)

    def _enriched_send_to_chat(self,
                               message: Union[FeatureMessage, Message]) -> None:
        """
        :func:`_enriched_send_to_chat` enriches a :class:`FeatureMessage`
        produced by a Feature, by adding the room's address to the Message
        if one is not already present.

        This method essentially handles converting a :class:`FeatureMessage`,
        where a room address is optional, to a :class:`Message`, where a room
        address is mandatory.

        This allows certain :class:`Feature` classes that may need to know
        about room addresses to send messages to specific rooms, while also
        allowing a :class:`Feature` to ignore any details about the specific
        room it is talking to if it wishes.
        """
        forward_msg = Message(message.text, message.room, data=message.data)
        if message.room is None:
            forward_msg.room = self.address
        self._send_to_chat(forward_msg)


class Bot:
    """
    The :class:`Bot` is the entrypoint to the application.

    The Bot class takes an instantiated :class:`~chatter_py.chat_client.ChatClient`
    and a collection of :class:`~chatter_py.feature.Feature` classes. The bot
    handles instantiating the `Features`, segregating them into individual
    :class:`~Room` objects.
    When a :class:`~chatter_py.message.Message` is forwarded by the `ChatClient`,
    the `Bot` will send it to the corresponding `Room` for further processing by
    the appropriate `Feature`.

    :param chat_client: The `ChatClient` that the bot will receive `Messages`
        from
    :param feature_classes: The :class:`~chatter_py.feature.Feature` classes that
        will be enabled for each :class:`~Room`
    :param config: config that is passed to all :class:`~Room` and
        :class:`~chatter_py.feature.Feature` classes
    :param room_class: The type of :class:`~Room` to use for routing. The
        default `Room` routes based on the first word of the `text` of a
        given :class:`~chatter_py.message.Message`. By subclassing `Room`,
        this routing logic can be changed.
    """

    def __init__(self,
                 chat_client: ChatClient,
                 feature_classes: Iterable[Type[Feature]],
                 config=None, room_class: Type[Room] = Room):
        self._chat_client: ChatClient = chat_client
        self._chat_client.send_to_bot = self._send_to_room

        self.rooms: Dict[str, Room] = {}

        self._features_types: Iterable[Type[Feature]] = feature_classes
        self._config = config
        self._room_class: Type[Room] = room_class

    def start(self) -> None:
        """
        Start the :class:`Bot`.

        Starting the `Bot` is a blocking call, and will cause the `Bot` to begin
        listening to the `ChatClient` and routing `Messages` to `Features`.
        """
        self._chat_client.start_listening()

    def _send_to_room(self, message: Message) -> None:
        """
        Send a message to a room. If a room does not exist, create the room
        first, then send the message to it.

        :param message: a Message to send to the Room
        """
        if message.room not in self.rooms.keys():
            self.rooms[message.room] = self._create_room(message.room)
        self.rooms[message.room].send_to_feature(message)

    def _create_room(self, address) -> Room:
        return self._room_class(self._features_types,
                                self._chat_client.send_to_client,
                                address,
                                self._config)
