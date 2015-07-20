from viewComponents.list           import List
from viewComponents.standardButton import StandardButton

class CathegoryList(List):

    def __init__(self, **kwargs):
        super(CathegoryList, self).__init__(**kwargs)
        self.register_event_type("on_cathegory_button_selected")

    #required by kivy
    def on_cathegory_button_selected(self, *args):
        pass

    def cathegory_button_pressed(self, word_button):
        self.dispatch("on_cathegory_button_selected", word_button.text)

    def build_list(self, cathegories):
        self.buttons.clear_widgets()

        for cathegory in cathegories:
            button = StandardButton(text=cathegory)
            button.bind(on_press = self.cathegory_button_pressed)
            self.buttons.add_widget(button)

        #highlight first element
        first_button = self.buttons.children[-self.FIRST_WORD_POS -1] #kivy orders children in reverse order
        first_button.highlight() 
        self.highlighted = self.FIRST_WORD_POS
        self.scroll_y    = 1
