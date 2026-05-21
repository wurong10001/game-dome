from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from main_menu import MainMenu
from test_level import TestLevel

class GameApp(App):
    def build(self):
        self.main_menu = MainMenu()
        self.main_menu.bind_events(self.on_start_game, self.on_settings)
        return self.main_menu

    def on_start_game(self, instance):
        # Switch to test level
        self.root.clear_widgets()
        self.root.add_widget(TestLevel())

    def on_settings(self, instance):
        # Placeholder for settings
        pass

if __name__ == "__main__":
    GameApp().run()
