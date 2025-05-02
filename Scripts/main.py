import sys
import os

# Добавляем родительскую директорию в sys.path, чтобы найти Scripts
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Scripts.game import Game

if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()
