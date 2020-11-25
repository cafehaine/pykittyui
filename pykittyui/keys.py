from enum import Enum
from queue import Queue
from sys import stdin
from threading import Thread
from typing import NamedTuple, Set, Union

from pykittyui.events import Event

class SpecialKey(Enum):
    """
    Some of kitty's special key codes.

    The full list is available here:
    https://sw.kovidgoyal.net/kitty/key-encoding.html
    """

    ESCAPE = "y"


class KeyEvent(Event):
    """A container for a key and a set of modifiers."""
    def __init__(self, key: Union[SpecialKey, str], modifiers: Set["Modifier"]):
        self.key = key
        self.modifiers = modifiers


class Modifier:
    pass


def _key_loop(output_queue: "Queue[Event]") -> None:
    """The loop run in a separate thread to create key events."""
    modifiers: Set[Modifier] = set()
    while True:
        key = stdin.read(1)
        if key == "\x1b":  # Kitty key code
            kitty_code = key
            while key != "\\":
                kitty_code += key
                key = stdin.read(1)
            kitty_code += key
            # TODO parse code
        else:
            output_queue.put(KeyEvent(key, modifiers))


def read_keys(output_queue: "Queue[Event]") -> None:
    """Spin up a thread that will push KeyEvents into a queue, reading stdin."""
    Thread(target=_key_loop, args=(output_queue,), daemon=True).start()
