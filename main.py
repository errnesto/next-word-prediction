from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty


class Root(FloatLayout):
  content  = ObjectProperty(None)

  def load_content(self):
    content = self.content
    for but in range(20):
      button = Button(text=str(but))
      content.add_widget(button)

class MainApp(App):

  def build(self):
    root = Root()
    root.load_content()
    return root

if __name__ == '__main__':
  MainApp().run()