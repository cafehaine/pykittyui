# PyKittyUi

PyKittyUI is an Open-Source low level python library to help you create TUIs in
Kitty.

I've made this in order to create applications with full keyboard support, as
specified in Kitty's protocol extensions.

It is licensed under the GPLv3 which means that any project using it *must* use
GPLv3 (from what I understand, I might be wrong, don't take my word for it).

## How to use it

Here's a really simplified program that uses PyKittyUi to draw some text:

```python
from pykittyui import Window

class HelloWorld(Window):
    def __init__(self):
        super().__init__()

    def draw(self):
        buff.draw_text(0, 0, "Press q to quit.")

    def on_key(self, event) -> None:
        if event.key == "q" and not event.modifiers:
            self.quit()

if __name__ == "__main__":
    window = HelloWorld()
    window.loop()
```

For more examples, check out the examples directory.
