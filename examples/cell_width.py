"""
Check if cell width works as expected.
"""

from pykittyui import Window
from pykittyui.keys import KeyEvent, SpecialKey

from examples.redrawspam import RedrawSpamThread


class CellWidth(Window):
    """A simple window that draws an hello world."""

    def __init__(self):
        super().__init__()
        self._mode = 1
        self._heart_x = 0
        self._thread = RedrawSpamThread(self._event_queue)

        self._thread.start()

    def draw_1(self):
        """Draw lines of alternating two cell and once cell characters."""
        char_even = "🧩"  # a two cell width character
        char_odd = "~"  # a one cell width character
        buff = self.get_buffer()
        width, height = self.get_dimensions()
        buff.draw_text(
            0,
            1,
            "Mode 1. You should see alternating rows of jigsaw pieces and tildes. ",
        )
        for y in range(1, height):
            if y % 2 == 0:
                buff.draw_text(0, y, char_even * (width // 2 - 1))
            else:
                buff.draw_text(0, y, char_odd * width)

    def draw_2(self):
        heart = "💙"  # a two cell width character
        buff = self.get_buffer()
        buff.draw_text(
            0,
            1,
            "Mode 2. You should see a blue heart move on a single line leaving no trail.",
        )
        width, _ = self.get_dimensions()
        self._heart_x = (self._heart_x + 1) % (width)
        buff.draw_text(self._heart_x, 3, heart)

    def draw(self):
        """Draw the screen."""
        buff = self.get_buffer()
        buff.draw_text(0, 0, "Press 'q' or escape to quit. Press 1-2 to select a mode.")
        if self._mode == 1:
            self.draw_1()
        else:
            self.draw_2()

    def on_key(self, combo: KeyEvent) -> None:
        if combo.key in ("q", SpecialKey.ESCAPE) and not combo.modifiers:
            self.quit()
        elif combo.key in ("1", "2") and not combo.modifiers:
            self._mode = int(combo.key)
            self._thread.set_spam(self._mode == 2)
            self.get_buffer().clear()
            self.redraw()


if __name__ == "__main__":
    window = CellWidth()
    window.loop()
