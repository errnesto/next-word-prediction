from kivy.uix.scrollview import ScrollView
from kivy.properties     import ObjectProperty
from kivy.lang           import Builder
Builder.load_file('viewComponents/List.kv')

class List(ScrollView):
  FIRST_WORD_POS = 0
  highlighted    = FIRST_WORD_POS
  buttons        = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(List, self).__init__(**kwargs)

  def move_highlight(self, direction):
    if direction == 'right':
      self.highlighted += 1
    else:
      self.highlighted -= 1

    if self.highlighted >= len(self.buttons.children):
      self.highlighted = self.FIRST_WORD_POS
    elif self.highlighted < 0:
      self.highlighted = len(self.buttons.children) -1

    for i, button in enumerate(reversed(self.buttons.children)):
      if (i == self.highlighted):
        button.highlight()
        self.scroll_to(button)
      else:
        button.unhighlight()

  def select_current(self):
    for i, button in enumerate(reversed(self.buttons.children)):
      if (i == self.highlighted):
        button.dispatch('on_press')
        break
