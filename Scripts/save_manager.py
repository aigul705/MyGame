import json
import os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
savefile = "savegame.json"
save1 = os.path.join(base, savefile)

def get_game_state(game_instance):
    """
    Извлекает состояние из экземпляра игры.
    args: game_instance - "объект" игры
    return: координаты врагов, пуль, игрока + счёт

    """
    if not game_instance or not hasattr(game_instance, 'player'):
        return {}

    # Игрок и счёт
    state = {
        'player_pos': list(game_instance.player.rect.center),
        'score': getattr(game_instance, 'score', 0),
    }
    # Враги
    state['enemies'] = [list(enemy.rect.center) for enemy in game_instance.enemy_manager.enemies]
    # Пули
    state['bullets'] = [
        {
            'pos': list(bullet.rect.center),
            'velocity': list(bullet.velocity)
        }
        for bullet in game_instance.enemy_manager.bullets
    ]
    return state

def save_game(game_state):
    """Сохраняет переданное состояние игры в файл.
    args:game_state - словарь, содержащий данные игры (позиции игрока, врагов, пуль, счёт)
    return: записаные данные в файл savegame"""

    try:
        with open(save1, 'w') as f:
            json.dump(game_state, f, indent=4)
    except Exception as e:
        print("Ошибка в save")

def load_game():
    """Загружает состояние игры из файла.
    return: даные из файла savegame"""
    
    with open(save1, 'r') as f:
        state_data = json.load(f)
    return state_data


def loaded_state(game_instance, state_data):
    """Применяет загруженное состояние к игре
    args: game_instance - объект игры
          state_data - сохранённые данные из файла savegame
    """

    try:
        # Игрок
        player_pos_list = state_data.get('player_pos')
        game_instance.player.rect.center = tuple(player_pos_list)

        # счёт
        game_instance.score = state_data['score']

        # Враги
        for pos in state_data.get('enemies', []):
            from Scripts.vrag import Enemy
            enemy = Enemy(game_instance.screen_width, game_instance.screen_height, game_instance.player)
            enemy.rect.center = tuple(pos)
            game_instance.enemy_manager.enemies.add(enemy)#добавление в группу для дальнейших волн

        # Пули
        for b in state_data.get('bullets', []):
            from Scripts.vrag import Bullet
            bullet = Bullet(tuple(b['pos']), (0, 0))
            bullet.velocity = tuple(b['velocity'])
            game_instance.enemy_manager.bullets.add(bullet)#добавление в группу для дальнейших волн
    except Exception as e:
        print("Проблема с сохранённым файлом(")
       