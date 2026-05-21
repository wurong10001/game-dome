from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from test_level import TestLevel

class GameApp(App):
    def build(self):
        # 主菜单设置为 TestLevel 的 widget
        level = TestLevel()  # 生成关卡
        return level.get_widget()

from kivy.uix.floatlayout import FloatLayout

class GameApp(App):
    def build(self):
        # 简单布局，仅待后续扩展
        root = FloatLayout()
        return root
