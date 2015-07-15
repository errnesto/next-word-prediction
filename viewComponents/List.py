from kivy.uix.scrollview import ScrollView
from kivy.properties     import ObjectProperty
from kivy.lang           import Builder
Builder.load_file("viewComponents/list.kv")

class List(ScrollView):
    FIRST_WORD_POS = 0
    BUTTONS_IN_ROW = 5
    highlighted    = FIRST_WORD_POS
    buttons        = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)

    def move_highlight(self, direction):
        if direction in ["left", "right"]:
            if direction == "right":
                self.highlighted += 1
            else:
                self.highlighted -= 1

            if self.highlighted >= len(self.buttons.children):
                self.highlighted = self.FIRST_WORD_POS
            elif self.highlighted < 0:
                self.highlighted = len(self.buttons.children) -1

        elif direction in ["up", "down"] and self.highlighted >= self.FIRST_WORD_POS:
            old_pos = self.highlighted
            if direction == "down":
                self.highlighted += self.BUTTONS_IN_ROW
            else:
                self.highlighted -= self.BUTTONS_IN_ROW

            if self.highlighted >= len(self.buttons.children) or self.highlighted < self.FIRST_WORD_POS:
                self.highlighted = old_pos

        for i, button in enumerate(reversed(self.buttons.children)):
            if (i == self.highlighted):
                button.highlight()
                self.scroll_to(button)
            else:
                button.unhighlight()

    def select_current(self):
        for i, button in enumerate(reversed(self.buttons.children)):
            if (i == self.highlighted):
                button.dispatch("on_press")
                break
