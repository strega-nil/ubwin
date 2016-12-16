import tkinter.font
import tkinter as tk

from datetime import timedelta, datetime

class Wait:
  def __init__(self, microseconds = 1000000):
    self.period = timedelta(microseconds = microseconds)
    self.last_time = datetime.now() - self.period

  def us_since_last_update(self):
    return (datetime.now() - self.last_time).microseconds

  def wait(self):
    while not self.ready():
      pass

  def ready(self):
    if datetime.now() >= self.last_time + self.period:
      self.last_time = datetime.now() + self.period
      return True
    else:
      return False

class Window:
  def __init__(self, width, height, bindings = [], fps = 60):
    self.__root = tk.Tk()
    self.__canvas = tk.Canvas(self.__root, width = width, height = height)
    self.__canvas.pack()
    self.__fps_wait = Wait(microseconds = 1000000 / fps)
    self.__running = True
    for el in bindings:
      if el[0] == "<Destroy>":
        raise RuntimError("Attempted to rebind '<Destroy>', which \
          must always be a synonym for exit")
      self.__root.bind(el[0], el[1])

    self.__root.bind("<Destroy>", lambda ev: self.win_exit())

    self._width = width
    self._height = height

  def win_loop(self):
    try:
      while self.__running:
        self.__fps_wait.wait()
        self.update_and_draw()
        self.__root.update_idletasks()
        self.__root.update()

    except KeyboardInterrupt:
      self.win_exit()

  # USER CALLABLES
  def win_exit(self):
    self.exit()
    self.__running = False

  def win_clear(self):
    self.__canvas.delete(tk.ALL)

  def win_draw_rect(self, x, y, width, height, color = "black",
      outline_width = 0, outline = "black"):
    self.__canvas.create_rectangle(x, y, x + width, y + height,
      fill = color, width = outline_width, outline = outline)
  def win_draw_text(self, text, x, y):
    self.__canvas.create_text(x, y, text = text._text,
      font = text._font._tk_font(), anchor = tk.NW)
  def win_draw_line(self, x1, y1, x2, y2, color = "black", width = 1):
    self.__canvas.create_line(x1, y1, x2, y2, fill = color, width = width)

  def win_set_bg(self, color):
    self.__canvas.configure(background = color)

  def win_us_since_last_update(self):
    return self.__fps_wait.us_since_last_update()

  def win_width(self, width = None):
    if width is not None:
      self._width = width
      self.__canvas.config(width = width)
    return self._width

  def win_height(self, height = None):
    if height is not None:
      self._height = height
      self.__canvas.config(height = height)
    return self._height

  # OVERLOADS
  def update_and_draw(self):
    pass

  def exit(self):
    pass

# Only use after creating a Window
class Font:
  def __init__(self, family = "times", size = 12):
    self._family = family
    self._size = size

  def set_font_family(self, family):
    self._family = family
  def set_font_size(self, size):
    self._size = size
  def set_font(self, family, size):
    self._size = size
    self._family = family

  def _tk_font(self):
    return tk.font.Font(family = self._family, size = self._size)

  def width(self, text):
    return self._tk_font().measure(text)

  def height(self, text):
    font = self._tk_font()
    line_height = font.metrics("linespace")
    ret = line_height
    for char in text:
      if char == '\n':
        ret += line_height
    return ret

class Text:
  def __init__(self, text, color = "black", font = None):
    self._text = text
    self._color = color
    if font is None:
      self._font = Font()
    else:
      self._font = font

  def set_text(self, text):
    self._text = text
  def set_font(self, font):
    self._font = font
  def set_color(self, color):
    self._color = color

  def width(self):
    return self._font.width(self._text)
  def height(self):
    return self._font.height(self._text)

class TextBox:
    def __init__(self, text, x = 0, y = 0, textsize = 20):
      self._textsize = textsize
      self._text = text
      self._font = Font(size = self._textsize)
      self._x = x
      self._y = y

    def _text_object(self):
      return Text(self._text + " ",
          font = self._font)

    def replace_text(self, text):
      self._text = text

    def set_location(self, x, y):
      self._x = x
      self._y = y

    def draw(self, window):
      window.win_draw_rect(
        self._x,
        self._y,
        self.width(),
        self.height(),
        "white",
        outline_width = 1,
        outline = "black",
      )
      window.win_draw_text(
        self._text_object(),
        self._x + self._font.width(" ") // 2,
        self._y)

    def width(self):
      return self._text_object().width()

    def height(self):
      return self._text_object().height()

    def draw_line_to(self, other, window):
      if self._y + self.height() < other._y:
        window.win_draw_line(
            self._x + self.width() // 2, self._y + self.height(),
            other._x + other.width() // 2, other._y,
            color = "black",
            width = 1)
      elif other._y + other.height() < self._y:
        window.win_draw_line(
            other._x + other.width() // 2, other._y + other.height(),
            self._x + self.width() // 2, self._y + self.height(),
            color = "black",
            width = 1)
      elif self._x + self.width() < other._x:
        window.win_draw_line(
            self._x + self.width(), self._y + self.height() // 2,
            other._x, other._y + other.height() // 2,
            color = "black",
            width = 1)
      elif other._x + other.width() < self._x:
        window.win_draw_line(
            other._x + other.width(), other._y + other.height() // 2,
            self._x, self._y + self.height() // 2,
            color = "black",
            width = 1)
      else:
        # they're on top of each other
        pass
