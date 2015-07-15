from kivy.uix.boxlayout import BoxLayout
from kivy.properties    import ObjectProperty
from kivy.lang          import Builder

from models.wordPredictor          import WordPredictor
from viewComponents.wordList       import WordList
from viewComponents.cathegoryList  import CathegoryList
Builder.load_file('viewComponents/root.kv')

class Root(BoxLayout):
    word_predictor = WordPredictor()
    current_list   = None
    text_output    = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)

        self.show_cathegory_list()

    # this should easily be pluggable with any kind of input device
    # one should be able to expose the whole functionality of the app with the 3 signals "left" "right" and "enter"
    def signal_handler(self, signal):
        if signal in ["left", "right", "up", "down"]:
            self.current_list.move_highlight(signal)
        elif signal == 'enter':
            self.current_list.select_current()
        elif signal == 'del':
            self.word_deleted(self.current_list)
        elif signal == 'talk':
            self.talk(self.current_list)

    def talk(self, words_widget):
        # just empty out selected wors
        # no real talker integrated

        self.text_output.text = ""

        if words_widget.__class__.__name__ == "WordList":
            words      = self.word_predictor.getWordList()
            words_widget.build_list(words)

    def word_selected(self, words_widget, word):
        self.text_output.text = self.text_output.text + ' ' + word

        #generate next word list
        word_list = self.word_predictor.getWordList(word)
        words_widget.build_list(word_list)

    def word_deleted(self, words_widget):
        prev_words = self.text_output.text.split()
        if len(prev_words) <= 0:
            return
            
        prev_words.pop()
        self.text_output.text = " ".join(prev_words)

        if words_widget.__class__.__name__ == "WordList":
            prev_word  = prev_words[-1] if len(prev_words) > 0 else None
            words      = self.word_predictor.getWordList(prev_word)
            words_widget.build_list(words)

    def show_cathegory_list(self, words_widget = None):
        if words_widget:
            self.remove_widget(words_widget)

        cathegories = self.word_predictor.categories
        cathegory_widget = CathegoryList()
        cathegory_widget.build_list(cathegories)

        #listen to cathegory list
        cathegory_widget.bind(on_cathegory_button_selected = self.show_word_list)

        self.add_widget(cathegory_widget)
        self.current_list = cathegory_widget

    def show_word_list(self, cathegory_widget, category):
        self.word_predictor.go_to_categorie(category)
        self.remove_widget(cathegory_widget)

        #build initial list
        prev_words = self.text_output.text.split()
        prev_word  = prev_words[-1] if len(prev_words) > 0 else None
        words      = self.word_predictor.getWordList(prev_word)

        words_widget = WordList()
        words_widget.build_list(words)

        #listen to word list
        words_widget.bind(on_word_button_selected   = self.word_selected)
        words_widget.bind(on_delete_button_selected = self.word_deleted)
        words_widget.bind(on_back_button_selected   = self.show_cathegory_list)
        words_widget.bind(on_talk_button_selected   = self.talk)

        self.add_widget(words_widget)
        self.current_list = words_widget
