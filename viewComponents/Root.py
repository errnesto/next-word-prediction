from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from models.WordPredictor import WordPredictor
from viewComponents.WordList import WordList
Builder.load_file('viewComponents/Root.kv')

class Root(BoxLayout):
  word_list_wrapper = ObjectProperty(None)
  text_output       = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(BoxLayout, self).__init__(**kwargs)

    #build initial list
    self.word_predictor = WordPredictor()
    words = self.word_predictor.getWordList()

    self.word_list_wrapper = WordList()
    self.word_list_wrapper.build_list(words)
    self.add_widget(self.word_list_wrapper)

    #listen to word list
    self.word_list_wrapper.bind(on_button_selected = self.word_selected)

    #add key listeners
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down = self._keyboard_dispatcher)

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down = self._on_keyboard_down)
    self._keyboard = None

  def _keyboard_dispatcher(self, keyboard, keycode, text, modifiers):
    self.signal_handler(keycode[1]) #we use the kivy keycodes as signal names

  # this should easily be pluggable with any kind of input device
  # one should be able to expose the whole functionality of the app with the 3 signals "left" "right" and "enter"
  def signal_handler(self, signal):
    if signal == 'left':
      self.word_list_wrapper.move_highlight('left')
    elif signal == 'right':
      self.word_list_wrapper.move_highlight('right')
    elif signal == 'enter':
      self.word_list_wrapper.select_current()

  def word_selected(self, word_list_wrapper, word):
    self.text_output.text = self.text_output.text + ' ' + word

    #generate next word list
    words = self.word_predictor.getWordList()
    self.word_list_wrapper.build_list(words)
