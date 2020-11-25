from pykittyui import Window
from pykittyui.keys import KeyEvent, SpecialKey


class HelloWorld(Window):
    """A simple window that draws an hello world."""

    def __init__(self):
        super().__init__()
        self.text = "Hello World!"

    def draw(self):
        """Draw Hello World! on the screen."""
        buff = self.get_buffer()
        buff.clear()
        width, height = self.get_dimensions()
        x = width // 2 - len(self.text) // 2
        y = height // 2
        buff.draw_text(x, y, self.text)

    def on_key(self, combo: KeyEvent) -> None:
        if combo.key in ("q", SpecialKey.ESCAPE) and not combo.modifiers:
            self.quit()
        else:
            self.text = f"Key: {combo.key!r}. Press 'q' to exit."
            self.redraw()


if __name__ == "__main__":
    window = HelloWorld()
    window.loop()
