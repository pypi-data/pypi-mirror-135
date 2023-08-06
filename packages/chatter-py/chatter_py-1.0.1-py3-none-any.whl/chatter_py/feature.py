from inspect import signature
from typing import Tuple, Callable, Dict, List, Union

from chatter_py.message import Message, FeatureMessage


class _Subcommand:

    TRIGGERS = "subcommand_trigger_words-90aa7c63-a914"
    """This attribute needs to have an underlying random value so that it
    doesn't risk clashing with another attribute that has been set on a fn"""

    def __init__(self, *triggers: str):
        if len(triggers) == 0:
            raise TypeError("At least one trigger word must be provided!")
        self.triggers: Tuple[str, ...] = triggers

    def __call__(self, func: Callable[[Message], None]):
        if len(signature(func).parameters) != 2:
            raise TypeError(
                "A method decorated with subcommand must take two arguments,"
                " its instance (self), and the message to process."
                f" \"{func.__qualname__}\" has signature={signature(func)}"
            )
        setattr(func, subcommand.TRIGGERS, self.triggers)
        return func


subcommand = _Subcommand
"""
The subcommand decorator is used to indicate methods of a
:class:`Feature` that process a :class:`Message` if the first word
of the message matches the `triggers` given by the subcommand.

A subcommand's triggers are defined by passing parameters to the
subcommand decorator.

A subcommand can have multiple triggers, and different subcommands can
share a trigger word to allow for separation of concerns when processing
a message.

Note that for multiple methods sharing the same subcommand trigger,
no guarantee is made about the order the methods are called.

Example: ::

>>> class Poll(Feature):
>>>     @subcommand("create", "make")
>>>     def make_a_new_poll(self, message: Message):
>>>         # implementation to create a new poll

`Poll.make_a_new_poll` is called if the Poll feature receives a message
whose contents start with either the word 'create' or 'make'.
"""


class Feature:
    """
    A :class:`Feature` is the fundamental building block of your chat bot.

    A collection of :class:`Feature` classes makes up a :class:`Room`. A
    `Room` decides whether to route a given `Message` to a `Feature`.

    By default, for a :class:`Message` to be routed to your :class:`Feature`,
    the first word of the Message's text must match (case-insensitively) the
    `name` of your :class:`Feature`.  The default value for a Feature's name
    is the class name. For example ::

        >>> class Echo(Feature):
        ...     ...
        >>> Echo.name # "Echo"

    Subclasses of the :class:`Feature` class support using the
    :func:`subcommand` decorator. The `subcommand` decorator handles routing a
    `Message` to the methods defined within your `Feature` class ::

        >>> class Poll(Feature):
        ...     @subcommand("create", "make")
        ...     def create(self):
        ...         # create a poll
        ...
        ...     @subcommand("delete", "end", "stop")
        ...     def end(self):
        ...         # delete a poll

    The `Poll` class would automatically route a message based on the first word
    of its text to the relevant subcommand, or ignore it if no subcommand
    matches it.

    If the `subcommand` pattern does not suit your use case, you can implement
    your own custom Feature routing logic by overriding :func:`~Feature.handle`,
    for example ::

        >>> class Echo(Feature):
        ...     def handle(self, message):
        ...         # receive a message and send it back to the client
        ...         # with its original content
        ...         return_message = FeatureMessage(message.original_text)
        ...         self.send_to_chat(return_message)
    """
    def __init__(self, send_to_chat: Callable[[FeatureMessage], None],
                 config=None):
        self.subcommands = self._get_subcommand_map()
        self.send_to_chat = send_to_chat
        self.config = config

    @property
    def name(self) -> str:
        """The name of the command that will cause messages to be routed to
        this feature. By default, this is the class name, but can be
        overridden"""
        return self.__class__.__name__.lower()

    def handle(self, message: Union[Message, FeatureMessage]):
        """Handle a :class:`Message`. By default, handling a message involves
        invoking a relevant subcommand method based on the contents
        of the `Message`.

        For custom handling where using the `subcommand` decorator is not
        appropriate, this method should be overridden."""
        if message.text[0] in self.subcommands:
            cmd = message.text.pop(0)
            self.subcommands[cmd](message)

    def _get_subcommand_map(self) -> Dict[str, Callable[[Message], None]]:
        commands = self._get_all_subcommands()
        command_map = {}
        for command in commands:
            for trigger in getattr(command, subcommand.TRIGGERS):
                command_map[trigger.lower()] = command
        return command_map

    def _get_all_subcommands(self) -> List[Callable[[Message], None]]:
        user_commands = []
        for attr_name in dir(self):
            cls_attr = getattr(self, attr_name)
            if hasattr(cls_attr, subcommand.TRIGGERS):
                user_commands.append(cls_attr)
        return user_commands
