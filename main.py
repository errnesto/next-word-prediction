from kivy.app import App

from viewComponents.Root import *

class MainApp(App):

  def build(self):
    root = Root()
    root.load_content()
    return root

if __name__ == '__main__':
  MainApp().run()