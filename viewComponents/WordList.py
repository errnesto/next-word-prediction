from kivy.core.window    import Window
from kivy.uix.scrollview import ScrollView
from kivy.properties     import ObjectProperty
from kivy.lang           import Builder

from models.WordPredictor               import WordPredictor
from viewComponents.PredictedWordButton import PredictedWordButton
from viewComponents.BackButton          import BackButton
Builder.load_file('viewComponents/WordList.kv')

class WordList(ScrollView):
  FIRST_WORD_POS = 2
  highlighted    = FIRST_WORD_POS
  buttons        = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(WordList, self).__init__(**kwargs)
    self.register_event_type('on_button_selected')
    print(self.height)

  #default event handler
  def on_button_selected(self, *args):
    pass

  def button_pressed(self, button):
    self.dispatch('on_button_selected', button.text)

  def build_list(self, words):
    self.buttons.clear_widgets()

    back_button   = BackButton('BACK')
    delete_button = BackButton('DEL')
    # button.bind(on_press = self.button_pressed)
    self.buttons.add_widget(back_button)
    self.buttons.add_widget(delete_button)

    for word in words:
      button = PredictedWordButton(text = word)
      button.bind(on_press = self.button_pressed)
      self.buttons.add_widget(button)

    #highlight first element
    self.buttons.children[-self.FIRST_WORD_POS-1].highlight() #kivy orders children in reverse order
    self.highlighted = self.FIRST_WORD_POS

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
        self.dispatch('on_button_selected', button.text)
        break
