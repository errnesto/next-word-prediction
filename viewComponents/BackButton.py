from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout    import StackLayout
from kivy.properties         import ObjectProperty
from kivy.lang               import Builder
Builder.load_file('viewComponents/BackButton.kv')

class BackButton(RelativeLayout):
    button = ObjectProperty(None)
    red    = (1, 0.2, 0.2, 1)

    def __init__(self, text, **kwargs):
        super(BackButton, self).__init__(**kwargs)
        self.button.text = text

        self.register_event_type('on_press')
        self.register_event_type('on_release')
        self.button.bind(on_release = self.dispatch_on_press)

    def on_press(self, *args):
        pass
    def on_release(self, *args):
        pass

    def dispatch_on_press(self, *args):
        self.dispatch('on_press')
    
    def highlight(self):
        self.button.background_color = (1, 0.2, 0.2, 0.6)

    def unhighlight(self):
        self.button.background_color = self.red
