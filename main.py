import os
os.environ['MODERNGL_BACKEND']='es2'
from game_app import GameApp

if __name__ == "__main__":
    GameApp().run()
