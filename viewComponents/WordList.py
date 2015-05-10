from kivy.core.window import Window
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder

from models.WordPredictor import WordPredictor
from viewComponents.PredictedWordButton import PredictedWordButton
from viewComponents.BackButton import BackButton
Builder.load_file('viewComponents/WordList.kv')

class WordList(StackLayout):
  FIRST_WORD_POS = 2
  highlighted    = FIRST_WORD_POS

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

    back_button   = BackButton('BACK')
    delete_button = BackButton('DEL')
    # button.bind(on_press = self.button_pressed)
    self.add_widget(back_button)
    self.add_widget(delete_button)

    for word in words:
      button = PredictedWordButton(text = word)
      button.bind(on_press = self.button_pressed)
      self.add_widget(button)

    #highlight first element
    self.children[-self.FIRST_WORD_POS-1].highlight() #kivy orders children in reverse order
    self.highlighted = self.FIRST_WORD_POS

  def move_highlight(self, direction):
    if direction == 'right':
      self.highlighted += 1
    else:
      self.highlighted -= 1

    if self.highlighted >= len(self.children):
      self.highlighted = self.FIRST_WORD_POS
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
