# boxlayout.py
class BoxLayout:
    def __init__(self, orientation='vertical', spacing=0, size_hint=(1,1), pos_hint=None):
        self.orientation = orientation
        self.spacing = spacing
        self.size_hint = size_hint
        self.pos_hint = pos_hint
        self.children = []

    def add_widget(self, widget):
        self.children.append(widget)

    def clear_widgets(self):
        self.children.clear()
