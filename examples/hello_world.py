from pykittyui import Window
from pykittyui.keys import KeyCombo, Key, Modifier

class HelloWorld(Window):
    """A simple window that draws an hello world."""

    def draw(self, width: int, height: int):
        """Draw Hello World! on the screen."""
        text = "Hello World!"
        x = width // 2 - len(text) // 2
        y = height // 2
        self.get_buffer().draw_text(x, y, text)

    def on_key(self, combo: KeyCombo) -> None:
        if combo.key in (Key.ESCAPE, Key.Q) and not combo.modifiers:
            self.quit()
        elif combo.key in (Key.Q, Key.W) and Modifier.CTRL in combo.modifiers:
            self.quit()

if __name__ == "__main__":
    window = HelloWorld()
    window.loop()
