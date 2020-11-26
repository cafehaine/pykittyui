"""
Drawing speed test.

This is a really stupid example that scrolls text as fast as possible to test
performances.
"""

from pykittyui import Window
from pykittyui.keys import KeyEvent, SpecialKey

from examples.redrawspam import RedrawSpamThread


class SpeedTest(Window):
    """A window that scrolls a full page of text test the speed."""

    def __init__(self):
        super().__init__()
        self._line = 0
        with open(__file__, "r") as text:
            self._text = [line.rstrip() for line in text]
        self._scroll = False
        self._thread = RedrawSpamThread(self._event_queue)

        self._thread.start()

    def draw(self):
        """Draw the scrolling text."""
        buff = self.get_buffer()
        buff.clear()
        buff.draw_text(0, 0, "Press 's' to toggle the scrolling text.")
        buff.draw_text(0, 1, "Press 'q' or escape to quit.")
        if not self._scroll:
            return
        _width, height = self.get_dimensions()
        for y in range(2, height):
            buff.draw_text(0, y, self._text[(self._line + y - 2) % len(self._text)])
        self._line = (self._line + 1) % len(self._text)

    def on_key(self, combo: KeyEvent) -> None:
        if combo.key == "s" and not combo.modifiers:
            self._scroll = not self._scroll
            self._thread.set_spam(self._scroll)

        if combo.key in ("q", SpecialKey.ESCAPE) and not combo.modifiers:
            self.quit()


if __name__ == "__main__":
    window = SpeedTest()
    window.loop()
