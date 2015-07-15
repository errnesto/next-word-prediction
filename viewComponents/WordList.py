# coding=utf-8
from viewComponents.list           import List
from viewComponents.standardButton import StandardButton
from viewComponents.actButton   import ActButton

class WordList(List):
    FIRST_WORD_POS = 3

    def __init__(self, **kwargs):
        super(WordList, self).__init__(**kwargs)
        self.register_event_type('on_word_button_selected')
        self.register_event_type('on_delete_button_selected')
        self.register_event_type('on_back_button_selected')
        self.register_event_type('on_talk_button_selected')

    #default event handlers
    def on_word_button_selected(self, *args):
        pass
    def on_delete_button_selected(self, *args):
        pass
    def on_back_button_selected(self, *args):
        pass
    def on_talk_button_selected(self, *args):
        pass

    def word_button_pressed(self, word_button):
        self.dispatch('on_word_button_selected', word_button.text)
    def delete_button_pressed(self, delete_button):
        self.dispatch('on_delete_button_selected')
    def back_button_pressed(self, back_button):
        self.dispatch('on_back_button_selected')
    def talk_button_pressed(self, back_button):
        self.dispatch('on_talk_button_selected')

    def build_list(self, words):
        self.buttons.clear_widgets()

        talk_button   = ActButton('sprechen', color=(0.2, 1, 0.2, 1))
        delete_button = ActButton(u'löschen')
        back_button   = ActButton(u'Menu', color=(1, 1, 1, 1))
        
        back_button.bind(on_press   = self.back_button_pressed)
        delete_button.bind(on_press = self.delete_button_pressed)
        talk_button.bind(on_press = self.talk_button_pressed)
        self.buttons.add_widget(back_button)
        self.buttons.add_widget(delete_button)
        self.buttons.add_widget(talk_button)

        for word in words:
            button               = StandardButton(text = word)
            button.bind(on_press = self.word_button_pressed)
            self.buttons.add_widget(button)

        #highlight first element
        first_button = self.buttons.children[-self.FIRST_WORD_POS -1] #kivy orders children in reverse order
        first_button.highlight() 
        self.highlighted = self.FIRST_WORD_POS
        self.scroll_y    = 1
