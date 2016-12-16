import npmwin

class Window(npmwin.Window):
  def __init__(self, width, height, color, trie):
    npmwin.Window.__init__(
      self,
      width,
      height,
      bindings = [
        ("<Key>", lambda ev: self.keypress(ev.char)),
        ("<BackSpace>", lambda ev: self.backspace()),
      ],
    )
    self.color = color
    self.trie = trie
    self.win_set_bg(color)
    self.string = []

  def keypress(self, key):
    if key:
      self.string.append(key)
  
  def backspace(self):
    if self.string:
      self.string.pop()

  def update_and_draw(self):
    self.win_clear()
    self.win_set_bg(self.color)

    text = npmwin.TextBox(''.join(self.string), 10, 10)
    text.draw(self)

    self.trie.rebuild(self.string)
    self.trie.draw(self)

class Trie:
  #-------------------------- nested _Node class --------------------------
  class _Node:
    def __init__(self):
      self._dict = {}

    def add(self, word, start_idx = 0):
      if start_idx < len(word):
        c = word[start_idx]
        if c not in self._dict:
          self._dict[c] = Trie._Node()
        self._dict[c].add(word, start_idx + 1)

    def __iter__(self):
      yield from self._dict.items()

    def clear(self):
      self._dict.clear()

    # returns the textbox object
    def draw(self, letter, window, horiz, vert, rec = 0):
      textbox = npmwin.TextBox(letter, horiz, vert)
      textbox.draw(window)
      width = textbox.width()
      ret = horiz + width + 10

      for (letter, node) in self:
        (new_horiz, tb) = node.draw(
          letter, window, horiz, vert + textbox.height() + 10, rec + 1
        )
        if new_horiz > horiz:
          horiz = new_horiz
          ret = new_horiz
        textbox.draw_line_to(tb, window)

      return (ret, textbox)
    
    def __contains__(self, word, idx = 0):
      if word == "":
        return True
      else:
        return (
          word[idx] in self._dict
          and self._dict[word[idx]].__contains__(word, idx + 1)
        )
          
  def __init__(self):
    self._root = self._Node()

  def __iter__(self):
    yield from self._root

  def draw(self, window):
    self._root.draw('', window, 10, 50)
  
  def add(self, word):
    self._root.add(word)

  def __contains__(self, word):
    return word in self._root

  def rebuild(self, string):
    self._root.clear()
    for i in range(len(string)):
      self._root.add(string, i)

trie = Trie()
window = Window(1000, 1000, 'grey', trie)
window.win_loop()
