from viewComponents.List           import List
from viewComponents.StandardButton import StandardButton
from viewComponents.BackButton     import BackButton

class WordList(List):
  FIRST_WORD_POS = 2

  def __init__(self, **kwargs):
    super(WordList, self).__init__(**kwargs)
    self.register_event_type('on_word_button_selected')
    self.register_event_type('on_delete_button_selected')
    self.register_event_type('on_back_button_selected')

  #default event handlers
  def on_word_button_selected(self, *args):
    pass
  def on_delete_button_selected(self, *args):
    pass
  def on_back_button_selected(self, *args):
    pass

  def word_button_pressed(self, word_button):
    self.dispatch('on_word_button_selected', word_button.text)
  def delete_button_pressed(self, delete_button):
    self.dispatch('on_delete_button_selected')
  def back_button_pressed(self, back_button):
    self.dispatch('on_back_button_selected')


  def build_list(self, words):
    self.buttons.clear_widgets()

    back_button   = BackButton('BACK')
    delete_button = BackButton('DEL')
    
    back_button.bind(on_press   = self.back_button_pressed)
    delete_button.bind(on_press = self.delete_button_pressed)
    self.buttons.add_widget(back_button)
    self.buttons.add_widget(delete_button)

    for word in words:
      button               = StandardButton(text = word)
      button.bind(on_press = self.word_button_pressed)
      self.buttons.add_widget(button)

    #highlight first element
    first_button = self.buttons.children[-self.FIRST_WORD_POS -1] #kivy orders children in reverse order
    first_button.highlight() 
    self.highlighted = self.FIRST_WORD_POS
    self.scroll_y    = 1