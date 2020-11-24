from queue import Queue
from sys import stdin
from typing import NamedTuple, Set

class Key:
    pass

class KeyCombo(NamedTuple):
    """A container for a key and a set of modifiers."""
    key: Key
    modifiers: Set['Modifier']

class Modifier:
    pass

def read_keys(output_queue: 'Queue[KeyCombo]') -> None:
    """Spin up a thread that will push KeyCombos into a queue, reading stdin."""
    while True:
        key = stdin.read(1)
        output_queue.put(KeyCombo(Key(), set([Modifier()])))
