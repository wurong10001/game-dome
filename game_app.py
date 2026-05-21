from kivy.app import App
from main_menu import MainMenu
from test_level import TestLevel

class GameApp(App):
    def build(self):
        # 主菜单
        menu = MainMenu()
        menu.bind_events(self.on_start_game, self.on_settings)
        return menu

    def on_start_game(self, instance):
        # 进入测试关卡
        self.root.clear_widgets()
        test = TestLevel()
        self.root.add_widget(test)

    def on_settings(self, instance):
        # Placeholder
        pass

