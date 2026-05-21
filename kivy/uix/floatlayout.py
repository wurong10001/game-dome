# floatlayout.py
class FloatLayout:
    def __init__(self, **kwargs):
        self.children = []

    def add_widget(self, widget):
        self.children.append(widget)

    def clear_widgets(self):
        self.children.clear()
