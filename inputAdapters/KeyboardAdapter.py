'''Keyboard Adapter using kivy'''

from _SuperAdapter import SuperAdapter
from kivy.core.window import Window

class KeyboardAdapter(SuperAdapter):

  def __init__(self, **kwargs):
    super(KeyboardAdapter, self).__init__(**kwargs)

    #add key listeners
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down = self.signal_dispatcher)

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down = self.signal_dispatcher)
    self._keyboard = None

  def signal_dispatcher(self, keyboard, keycode, text, modifiers):
    # required signals are: 'left' 'right' and 'enter'
    if keycode[1] == 'left':
      self.dispatch('on_signal', 'left')
    elif keycode[1] == 'right':
      self.dispatch('on_signal', 'right')
    elif keycode[1] == 'enter':
      self.dispatch('on_signal', 'enter')

    #these are convenience signals which are not required
    elif modifiers and modifiers[0] == 'meta' and keycode[1] == 'q':
      self.dispatch('on_signal', 'close')

  @staticmethod
  def is_available():
    return True