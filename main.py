from kivy.app            import App
from viewComponents.Root import Root

import inputAdapters # see __init__.py how this is initialized 

class MainApp(App):

  def build(self):
    # listen to all avalable input devices
    for inputAdapter in inputAdapters.adapters:
      if inputAdapter.is_available():
        input_adapter = inputAdapter()
        input_adapter.bind(on_signal = self.signal_handler)

    self.root = Root()
    return self.root

  def signal_handler(self, signal_adapter, signal):
    # either handle signal here or pass it down to root object
    if signal == 'close':
      self.stop()
    else:
      self.root.signal_handler(signal)

if __name__ == '__main__':
  MainApp().run()
