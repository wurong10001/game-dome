import os
import datetime
from kivy.app import App
import logging

class DebugFileHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        # 尝试在手机根目录创建日志文件夹
        log_dir = '/storage/emulated/0/wurong/demo'
        try:
            os.makedirs(log_dir, exist_ok=True)
            # 使用下划线代替冒号，因为安卓系统文件名不支持冒号
            sub_dir = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
            full_dir = os.path.join(log_dir, sub_dir)
            os.makedirs(full_dir, exist_ok=True)
            log_file = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_demo_boot.log')
            self.log_path = os.path.join(full_dir, log_file)
            self.setLevel(logging.DEBUG)
        except Exception as e:
            print(f"无法创建日志文件夹，可能是缺少存储权限: {e}")
            self.log_path = None

    def emit(self, record):
        if not self.log_path:
            return
        try:
            log_entry = self.format(record) + '\n'
            # 确保目录存在
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception:
            # 避免日志写入失败导致程序崩溃
            pass

class GameApp(App):
    def build(self):
        # 配置日志系统
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # 添加文件日志处理器
        file_handler = DebugFileHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 同时输出到控制台（方便用 logcat 查看）
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.debug('GameApp build started')

        # 主菜单
        try:
            menu = MainMenu()
            menu.bind_events(self.on_start_game, self.on_settings)
            logger.debug('MainMenu loaded successfully')
            return menu
        except Exception as e:
            logger.error(f"Failed to load MainMenu: {e}")
            # 如果菜单加载失败，返回一个空界面防止直接闪退
            from kivy.uix.label import Label
            return Label(text=f"Error loading menu:\n{e}")

    def on_start_game(self, instance):
        logging.debug('Start game pressed')
        try:
            # 进入测试关卡
            self.root.clear_widgets()
            test = TestLevel()
            self.root.add_widget(test)
            logging.debug('TestLevel loaded successfully')
        except Exception as e:
            logging.error(f"Failed to load TestLevel: {e}")

    def on_settings(self, instance):
        logging.debug('Settings pressed')
        # 设置功能占位
        pass

