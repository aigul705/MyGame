# Scripts/save_manager.py
import json
import os

# Определяем путь к файлу сохранения относительно ЭТОГО файла
# Поднимаемся на один уровень вверх (из Scripts в корень проекта)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_FILE_NAME = "savegame.json"
SAVE_FILE_PATH = os.path.join(BASE_DIR, SAVE_FILE_NAME)

def get_game_state(game_instance):
    """
    Извлекает состояние из экземпляра игры.
    Пока только позиция игрока.
    """
    if not game_instance or not hasattr(game_instance, 'player'):
        return {} # Возвращаем пустой словарь, если что-то не так

    state = {
        'player_pos': list(game_instance.player.rect.center)
        # Добавьте сюда другие данные для сохранения
    }
    return state

def save_game(game_state):
    """Сохраняет переданное состояние игры в файл."""
    if not game_state:
        print("Ошибка сохранения: нет данных для сохранения.")
        return
    try:
        with open(SAVE_FILE_PATH, 'w') as f:
            json.dump(game_state, f, indent=4)
        print(f"Игра сохранена в {SAVE_FILE_PATH}")
    except Exception as e:
        print(f"Ошибка сохранения игры в {SAVE_FILE_PATH}: {e}")

def load_game():
    """Загружает состояние игры из файла."""
    print(f"--- SM: Попытка загрузки из {SAVE_FILE_PATH} ---")
    if not os.path.exists(SAVE_FILE_PATH):
        print(f"--- SM: Файл сохранения {SAVE_FILE_PATH} не найден. ---")
        return None # Возвращаем None, если файла нет

    try:
        with open(SAVE_FILE_PATH, 'r') as f:
            state_data = json.load(f)
        print(f"--- SM: Состояние игры успешно загружено из JSON: {state_data} ---")
        return state_data
    except Exception as e:
        print(f"--- SM: Ошибка загрузки состояния из {SAVE_FILE_PATH}: {e}. ---")
        return None # Возвращаем None при ошибке чтения

def apply_loaded_state(game_instance, state_data):
    """Применяет загруженное состояние к экземпляру игры."""
    print(f"--- SM apply_loaded_state: Применение данных {state_data} к game_instance ---")
    if not game_instance or not state_data:
        print("--- SM apply_loaded_state: Экземпляр игры или данные отсутствуют. ---")
        return

    try:
        # Загружаем позицию игрока
        player_pos_list = state_data.get('player_pos')
        if player_pos_list and hasattr(game_instance, 'player'):
             game_instance.player.rect.center = tuple(player_pos_list)
             print(f"--- SM apply_loaded_state: Позиция игрока установлена в {game_instance.player.rect.center} ---")
        else:
             if hasattr(game_instance, 'player'):
                 default_pos = (game_instance.screen_width // 2, game_instance.screen_height // 2)
                 game_instance.player.rect.center = default_pos
                 print(f"--- SM apply_loaded_state: Позиция игрока не найдена в данных или нет игрока, установлена по умолчанию: {default_pos} ---")
             else:
                  print("--- SM apply_loaded_state: Экземпляр игры не имеет атрибута player. ---")

        # Загрузите здесь другие данные, применяя их к game_instance
        # print(f"Состояние применено: игрок в {getattr(game_instance.player, 'rect', {}).get('center', 'N/A')}") # Старый print

    except Exception as e:
        print(f"--- SM apply_loaded_state: Ошибка применения загруженного состояния: {e}. ---")
        # Можно добавить сброс к состоянию по умолчанию, если нужно
        if hasattr(game_instance, 'player'):
            game_instance.player.rect.center = (game_instance.screen_width // 2, game_instance.screen_height // 2) 