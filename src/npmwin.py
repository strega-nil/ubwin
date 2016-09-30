import tkinter as tk
from datetime import timedelta, datetime

class Wait:
  def __init__(self, microseconds = 1000000):
    self.period = timedelta(microseconds = microseconds)
    self.last_time = datetime.now() - self.period

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
  def __init__(self, width, height, fps = 60):
    self.__root = tk.Tk()
    self.__canvas = tk.Canvas(self.__root, width = width, height = height)
    self.__canvas.pack()
    self.__fps_wait = Wait(microseconds = 1000000 / fps)
    self.__running = True

  def loop(self, bindings = []):
    try:
      for el in bindings:
        if el[0] == "q" or el[0] == "<Destroy>":
          raise RuntimError("Attempted to rebind 'q' or '<Destroy>', which \
            must always be synonyms for exit")
        self.__root.bind(el[0], el[1])

      self.__root.bind("q", lambda ev: self.exit())
      self.__root.bind("<Destroy>", lambda ev: self.exit())

      while self.__running:
        self.__fps_wait.wait()
        self.update_and_draw()
        self.__root.update_idletasks()
        self.__root.update()

    except KeyboardInterrupt:
      pass

  # USER CALLABLES
  def exit(self):
    self.__running = False

  def clear(self):
    self.__canvas.delete(tk.ALL)

  def draw_rect(self, x, y, width, height, fill):
    self.__canvas.create_rectangle(x, y, x + width, y + height,
      fill = fill, outline = fill)

  # OVERLOADS
  def update_and_draw(self):
    pass

