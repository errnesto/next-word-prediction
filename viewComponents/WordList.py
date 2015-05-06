from kivy.core.window import Window
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder

from models.WordPredictor import WordPredictor
from viewComponents.PredictedWordButton import PredictedWordButton
Builder.load_file('viewComponents/WordList.kv')

class WordList(StackLayout):
  highlighted = 0

  def __init__(self, **kwargs):
    super(WordList, self).__init__(**kwargs)
    self.register_event_type('on_button_selected')

  #default event handler
  def on_button_selected(self, *args):
    pass

  def button_pressed(self, button):
    self.dispatch('on_button_selected', button.text)

  def build_list(self, words):
    self.clear_widgets()

    for word in words:
      button = PredictedWordButton(text = word)
      button.bind(on_press = self.button_pressed)
      self.add_widget(button)

    #highlight first element
    self.children[-1].highlight() #kivy orders children in reverse order

  def move_highlight(self, direction):
    if direction == 'right':
      self.highlighted += 1
    else:
      self.highlighted -= 1

    if self.highlighted >= len(self.children):
      self.highlighted = 0
    elif self.highlighted < 0:
      self.highlighted = len(self.children) -1

    for i, button in enumerate(reversed(self.children)):
      if (i == self.highlighted):
        button.highlight()
      else:
        button.unhighlight()

  def select_current(self):
    for i, button in enumerate(reversed(self.children)):
      if (i == self.highlighted):
        self.dispatch('on_button_selected', button.text)
        break

    self.highlighted = 0


