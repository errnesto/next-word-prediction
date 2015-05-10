from kivy.app           import App
from kivy.core.window   import Window

from viewComponents.Root  import *
from models.WordPredictor import *

class MainApp(App):

  def build(self):
    self.root = Root()
    #add key listeners
    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    self._keyboard.bind(on_key_down = self._keyboard_dispatcher)
    return self.root

  def _keyboard_closed(self):
    self._keyboard.unbind(on_key_down = self._on_keyboard_down)
    self._keyboard = None

  def _keyboard_dispatcher(self, keyboard, keycode, text, modifiers):
    # close on meta + q
    if modifiers and modifiers[0] == 'meta' and keycode[1] == 'q':
      self.stop()

    self.root.signal_handler(keycode[1]) #we use the kivy keycodes as signal names

if __name__ == '__main__':
  MainApp().run()
