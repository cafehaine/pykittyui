"""
Check if cell width works as expected.

If everything works, it should show a pattern like this:

🧩🧩🧩
~~~~~~
🧩🧩🧩
"""

from pykittyui import Window
from pykittyui.keys import KeyEvent, SpecialKey


class CellWidth(Window):
    """A simple window that draws an hello world."""

    def draw(self):
        """Draw lines of alternating two cell and once cell characters."""
        char_even = "🧩" # a two cell width character
        char_odd = "~" # a one cell width character
        buff = self.get_buffer()
        buff.clear()
        width, height = self.get_dimensions()
        buff.draw_text(0, 0, "Press 'q' or escape to quit.")
        for y in range(1, height):
            if y % 2 == 0:
                buff.draw_text(0, y, char_even * (width//2 - 1))
            else:
                buff.draw_text(0, y, char_odd * width)

    def on_key(self, combo: KeyEvent) -> None:
        if combo.key in ("q", SpecialKey.ESCAPE) and not combo.modifiers:
            self.quit()
        else:
            self.text = f"Key: {combo.key!r}. Press 'q' to exit."
            self.redraw()


if __name__ == "__main__":
    window = CellWidth()
    window.loop()
