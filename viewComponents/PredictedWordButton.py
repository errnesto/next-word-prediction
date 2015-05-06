from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_file('viewComponents/PredictedWordButton.kv')

class PredictedWordButton(Button):
  
  def highlight(self):
    self.background_color = (1, 1, 1, 0.5)

  def unhighlight(self):
    self.background_color = (1, 1, 1, 1)

