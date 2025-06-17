import pygame
import sys
import os

# Добавляем родительскую директорию в sys.path для корректных импортов
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) # Вставляем путь в начало

#  импортируем функцию главного меню
from Scripts.menu import main_menu_loop

if __name__ == '__main__':
    main_menu_loop()
    pygame.quit()
    sys.exit() 