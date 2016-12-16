UB Window Library
---

An easy-to-use windowing library for Python, based on Tk

In order to install, run

```shell
pip install git+https://github.com/ubsan/ubwin
```

Then use from your python files by writing:

```python
from ubwin import Window

class Foo(Window):
  def __init__(self, width, height):
    Window.__init__(self, width, height, fps = 60)

  def update_and_draw(self):
    pass
    # do what you need to do in order to update and draw

  def foo(self):
    print("hi!")

  def loop(self):
    Window.loop(self, (
      ("f", lambda ev: self.foo()),
      # ...
    ))
```
