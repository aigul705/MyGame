import json
import os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
savefile = "savegame.json"
save1 = os.path.join(base, savefile)

def get_game_state(game_instance):
    """
    Извлекает состояние из экземпляра игры.

    """
    if not game_instance or not hasattr(game_instance, 'player'):
        return {}

    # Игрок
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
    """Сохраняет переданное состояние игры в файл."""
    if not game_state:
        return
    try:
        with open(save1, 'w') as f:
            json.dump(game_state, f, indent=4)
    except Exception as e:
        print("Ошибка в save")

def load_game():
    """Загружает состояние игры из файла."""
    if not os.path.exists(save1):
        return None

    try:
        with open(save1, 'r') as f:
            state_data = json.load(f)
        return state_data
    except Exception as e:
        return None

def loaded_state(game_instance, state_data):
    """Применяет загруженное состояние к игре"""
    if not game_instance or not state_data:
        return
    try:
        # Игрок
        player_pos_list = state_data.get('player_pos')
        if player_pos_list and hasattr(game_instance, 'player'):
            game_instance.player.rect.center = tuple(player_pos_list)

        # Восстанавливаем счёт
        if 'score' in state_data:
            game_instance.score = state_data['score']

        # Враги
        game_instance.enemy_manager.enemies.empty()
        for pos in state_data.get('enemies', []):
            from Scripts.vrag import Enemy
            enemy = Enemy(game_instance.screen_width, game_instance.screen_height, game_instance.player)
            enemy.rect.center = tuple(pos)
            game_instance.enemy_manager.enemies.add(enemy)

        # Пули
        game_instance.enemy_manager.bullets.empty()
        for b in state_data.get('bullets', []):
            from Scripts.vrag import Bullet
            bullet = Bullet(tuple(b['pos']), (0, 0))
            bullet.velocity = tuple(b['velocity'])
            game_instance.enemy_manager.bullets.add(bullet)
    except Exception as e:
        if hasattr(game_instance, 'player'):
            game_instance.player.rect.center = (game_instance.screen_width // 2, game_instance.screen_height // 2) 