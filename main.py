from kivy.app import App

from viewComponents.Root import *
from models.WordPredictor import *

class MainApp(App):

  def build(self):
    return Root()

if __name__ == '__main__':
  MainApp().run()