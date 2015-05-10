from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('viewComponents/BackButton.kv')

class BackButton(RelativeLayout):
  button = ObjectProperty(None)
  red    = (1, 0.2, 0.2, 1)

  def __init__(self, text, **kwargs):
    super(BackButton, self).__init__(**kwargs)
    self.button.text = text
  
  def highlight(self):
    self.button.background_color = (1, 0.2, 0.2, 0.6)

  def unhighlight(self):
    self.button.background_color = self.red

