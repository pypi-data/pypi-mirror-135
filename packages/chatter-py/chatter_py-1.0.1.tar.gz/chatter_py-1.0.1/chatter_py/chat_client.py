from abc import abstractmethod, ABC
from typing import Callable

from chatter_py.message import Message


class ChatClient(ABC):
    """
    A :class:`ChatClient` handles receiving messages from a chat system,
    (typically through registering some callbacks), transforming these into
    :class:`~chatter_py.message.Message` format for the chatbot to understand,
    and forwarding these on.

    Any subclass of `ChatClient` must implement two methods:

    * `send_to_client`: allow the bot to send `Messages` to the chat client
    * `start_listening`: allow the bot to begin listening to the chat client
    """

    send_to_bot: Callable[[Message], None]
    """A method passed to the :class:`~ChatClient` by the
    :class:`~chatter_py.bot.Bot` that allows the `ChatClient` to forward
    messages to it."""

    @abstractmethod
    def send_to_client(self, message: Message):
        """
        Send a :class:`~chatter_py.message.Message` to the chat client.

        Converting the `Message` into a suitable format for the chat
        client is up to the implementing class.
        """

    @abstractmethod
    def start_listening(self) -> None:
        """
        Begin listening to the chat client for messages.

        To forward a message from the chat client to the bot, the message
        must be converted into a :class:`~chatter_py.message.Message` and sent
        using :func:`send_to_bot`.
        """
