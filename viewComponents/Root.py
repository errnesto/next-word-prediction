from kivy.uix.boxlayout import BoxLayout
from kivy.properties    import ObjectProperty
from kivy.lang          import Builder

import inputAdapters # see __init__.py how this is initialized 

from models.WordPredictor          import WordPredictor
from viewComponents.WordList       import WordList
from viewComponents.CathegoryList  import CathegoryList
Builder.load_file('viewComponents/Root.kv')

class Root(BoxLayout):
  word_predictor = WordPredictor()
  current_list   = None
  text_output    = ObjectProperty(None)

  def __init__(self, **kwargs):
    super(Root, self).__init__(**kwargs)

    # listen to all avalable input devices
    for inputAdapter in inputAdapters.adapters:
      if inputAdapter.is_available():
        input_adapter = inputAdapter()
        input_adapter.bind(on_signal = self.signal_handler)

    self.show_cathegory_list()

  # this should easily be pluggable with any kind of input device
  # one should be able to expose the whole functionality of the app with the 3 signals "left" "right" and "enter"
  def signal_handler(self, signal_adapter, signal):
    if signal == 'left':
      self.current_list.move_highlight('left')
    elif signal == 'right':
      self.current_list.move_highlight('right')
    elif signal == 'enter':
      self.current_list.select_current()

  def word_selected(self, words_widget, word):
    self.text_output.text = self.text_output.text + ' ' + word

    #generate next word list
    words = self.word_predictor.getWordList()
    words_widget.build_list(words)

  def word_deleted(self, words_widget):
    words = self.text_output.text.split(' ')
    words.pop()
    self.text_output.text = ' '.join(words)

  def show_cathegory_list(self, words_widget = None):
    if words_widget:
      self.remove_widget(words_widget)

    cathegory_widget = CathegoryList()
    cathegory_widget.build_list(['A', 'B', 'C'])

    #listen to cathegory list
    cathegory_widget.bind(on_cathegory_button_selected = self.show_word_list)

    self.add_widget(cathegory_widget)
    self.current_list = cathegory_widget

  def show_word_list(self, cathegory_widget, cathegory_button):
    self.remove_widget(cathegory_widget)

    #build initial list
    words = self.word_predictor.getWordList()

    words_widget = WordList()
    words_widget.build_list(words)

    #listen to word list
    words_widget.bind(on_word_button_selected   = self.word_selected)
    words_widget.bind(on_delete_button_selected = self.word_deleted)
    words_widget.bind(on_back_button_selected   = self.show_cathegory_list)

    self.add_widget(words_widget)
    self.current_list = words_widget
