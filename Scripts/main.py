import pygame
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 


from Scripts.menu import main_menu_loop

if __name__ == '__main__':
    main_menu_loop()
    pygame.quit()
    sys.exit() 