from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from viewComponents.PredictedWordButton import *
Builder.load_file('viewComponents/Root.kv')

class Root(FloatLayout):
  content  = ObjectProperty(None)

  def load_content(self):
    content = self.content
    for but in range(20):
      button = PredictedWordButton()
      content.add_widget(button)