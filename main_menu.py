from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp, sp

class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(20), size_hint=(0.8, 0.6),
                         pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.start_btn = Button(text="开始游戏", font_size=sp(24), size_hint=(1, 0.6),
                                 background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        self.settings_btn = Button(text="设置", font_size=sp(20), size_hint=(1, 0.4),
                                   background_color=(0.5, 0.5, 0.5, 1), color=(1, 1, 1, 1))
        self.add_widget(self.start_btn)
        self.add_widget(self.settings_btn)

    def bind_events(self, on_start, on_settings):
        self.start_btn.bind(on_press=on_start)
        self.settings_btn.bind(on_press=on_settings)
