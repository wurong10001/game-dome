import os
import datetime
from kivy.app import App
import logging

class DebugFileHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        log_dir = '/storage/emulated/0/wurong/demo'
        os.makedirs(log_dir, exist_ok=True)
        sub_dir = datetime.datetime.now().strftime('%Y:%m:%d：%H/%M')
        full_dir = os.path.join(log_dir, sub_dir)
        os.makedirs(full_dir, exist_ok=True)
        log_file = datetime.datetime.now().strftime('%Y:%m:%d：%H-%M-demo-boot.log')
        self.log_path = os.path.join(full_dir, log_file)
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        log_entry = self.format(record) + '\n'
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)

class GameApp(App):
    def build(self):
        # 配置日志
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        file_handler = DebugFileHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.debug('Game started in debug mode')

        # 主菜单
        from main_menu import MainMenu
        from test_level import TestLevel

        menu = MainMenu()
        menu.bind_events(self.on_start_game, self.on_settings)
        return menu

    def on_start_game(self, instance):
        logging.debug('Start game pressed')
        # 进入测试关卡
        self.root.clear_widgets()
        test = TestLevel()
        self.root.add_widget(test)

    def on_settings(self, instance):
        logging.debug('Settings pressed')
        # Placeholder
        pass

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

