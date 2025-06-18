import pygame
import os

# Получаем путь к корневой папке проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES_DIR = os.path.join(project_root, 'Sprites')

def load_sprite(sprite_name, with_alpha=False):
    """Загружает спрайт из папки Sprites.

    Args:
        sprite_name (str): Имя файла спрайта 
        with_alpha (bool, optional): Загружать ли с прозрачностью По умолчанию False.

    Returns:
        pygame.Surface: Загруженный спрайт
    """
    file_path = os.path.join(SPRITES_DIR, sprite_name)
    try:
        sprite = pygame.image.load(file_path)
    except pygame.error as e:
        raise SystemExit(e)

    if with_alpha:
        return sprite.convert_alpha()
    else:
        return sprite.convert() 