# Chatter

[![codecov](https://codecov.io/gh/nickjfenton/chatter/branch/develop/graph/badge.svg?token=4HYFV573S8)](https://codecov.io/gh/nickjfenton/chatter)
[![Documentation Status](https://readthedocs.org/projects/chatter-py/badge/?version=latest)](https://chatter-py.readthedocs.io/en/latest/?badge=latest)

## Welcome to Chatter!

Chatter is a framework with the goal of allowing you to quickly and easily create chatbots. It hides
away the things you want to just work, exposing a simple API, so that you can focus on writing your
custom features and delivering a working chatbot.

Take a look:

```python
from chatter_py import ChatClient, Feature, Bot, Message
from typing import Any


# Define your feature
class Echo(Feature):
    def receive(self, message):
        self.send_to_chat(message)


# Write a handler for your chat client, for example:
class MyChatClient(ChatClient):
    def __init__(self):
        self.chat_client_connection = Any

    def on_chat_message(self, message: dict):
        """Receive your chat messages and convert them to bot friendly messages"""
        bot_message = Message(text=message["text"], room=message["room_id"])
        self.send_to_bot(bot_message)

    def start_listening(self) -> None:
        """connect to your chat client"""
        self.chat_client_connection.register_callback(self.on_chat_message)
        self.chat_client_connection.start_listening()

    def send_to_client(self, message):
        """Format your bot messages and send them off to your chat client"""
        text = "<p>" + " ".join(message.text) + "</p>"
        self.chat_client_connection.send(text)


def main():
    # Let Chatter put it all together
    Bot(MyChatClient(), [Echo]).start()


if __name__ == '__main__':
    # Start your bot!
    main()
```

Chatter encourages you to separate concerns by keeping your chat client specific message
transformations in your `ChatClient` classes and letting all your `Feature` classes handle
standardised
`Messages`. This:

* Makes your code more testable
* Makes your bot super portable - being able to handle a new chat client is as simple as creating a
  new `ChatClient` subclass and writing your custom logic for transforming messages between Bot and
  Presentation format.

You could even use a command-line frontend for testing your bot's logic:

```python
from chatter_py import ChatClient, Message


class CommandLine(ChatClient):
    def send_to_client(self, message: Message):
        print("Chatter-bot: " + " ".join(message.text))

    def start_listening(self) -> None:
        while True:
            input_message = input("You: ")
            message_to_bot = Message(text=input_message.split(" "), room="")
            self.send_to_bot(message_to_bot)
```

Now every time you write a new chat client class, all you have to focus on testing is given a Bot
message, you receive the correct chat message, and vice versa - simple!
