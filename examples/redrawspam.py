"""
This module defines a RedrawSpamThread class that spams redraw events.

This is used in speed_test.py and cell_width.py.
"""

from queue import Queue
from threading import Thread, Lock
from time import sleep

from pykittyui.events import Event, RedrawEvent


class RedrawSpamThread(Thread):
    """A thread that spams 'RedrawEvent's in the given queue when told to."""

    def __init__(self, queue: "Queue[Event]"):
        super().__init__(daemon=True)
        self._should_spam = False
        self._lock = Lock()
        self._queue = queue

    def set_spam(self, should_spam: bool) -> None:
        """Set if the thread should spam redraws."""
        self._lock.acquire()
        self._should_spam = should_spam
        self._lock.release()

    def run(self) -> None:
        """The thread's main loop."""
        while True:
            self._lock.acquire()
            spam = self._should_spam
            if spam:
                self._queue.put(RedrawEvent())
            self._lock.release()
            if not spam:
                sleep(0.1)
            else:
                sleep(0.001)
