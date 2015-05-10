from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('viewComponents/BackButton.kv')

class BackButton(FloatLayout):
  button = ObjectProperty(None)
  red    = (1, 0.2, 0.2, 1)
  
  def highlight(self):
    self.button.background_color = (1, 0.2, 0.2, 0.6)

  def unhighlight(self):
    self.button.background_color = self.red

