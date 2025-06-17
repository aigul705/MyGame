import pygame
import sys
import os

# СНАЧАЛА добавляем родительскую директорию в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
# Вставляем путь в начало, чтобы он имел приоритет, если есть конфликты
sys.path.insert(0, parent_dir)

# ТЕПЕРЬ импортируем модули из Scripts
import Scripts.save_manager as save_manager
from Scripts.button import Button
from Scripts.game import Game
from Scripts import constant as const # Импортируем константы



# Инициализация Pygame и микшера
pygame.init()
pygame.mixer.init()

# Загрузка и настройка фоновой музыки
music_path = "Sprites/Player/music/Ghostrifter-Official-Resurgence(chosic.com).mp3"  # Используется и в меню, и в игре
try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.5)  # Устанавливаем громкость (от 0.0 до 1.0)
    pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение
except pygame.error as e:
    print(f"Не удалось загрузить музыку: {music_path}\n{e}")

# Настройки экрана (используем константы)
screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption("Главное Меню")

# Загрузка фонового изображения
background_image_path = "Sprites/Player/fon/swamp-illustration-vector.png"
try:
    background_image = pygame.image.load(background_image_path).convert()
    # Масштабируем изображение до размеров экрана
    background_image = pygame.transform.scale(background_image, (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Не удалось загрузить или масштабировать фоновое изображение: {background_image_path}\n{e}")
    # Установим резервный цвет фона, если изображение не загрузилось
    background_image = None # Или можно создать Surface с цветом const.WHITE

# Создание кнопок (используем константы)
total_height = const.BUTTON_HEIGHT * 3 + const.BUTTON_SPACING * 2 # Увеличиваем высоту для 3 кнопок
start_y = (const.SCREEN_HEIGHT - total_height) // 2

continue_button = Button(
    (const.SCREEN_WIDTH - const.BUTTON_WIDTH) // 2,
    start_y,
    const.BUTTON_WIDTH,
    const.BUTTON_HEIGHT,
    "Продолжить игру",
    const.GRAY, const.LIGHT_GRAY, const.BLACK
)

new_game_button = Button(
    (const.SCREEN_WIDTH - const.BUTTON_WIDTH) // 2,
    start_y + const.BUTTON_HEIGHT + const.BUTTON_SPACING,
    const.BUTTON_WIDTH,
    const.BUTTON_HEIGHT,
    "Новая игра",
    const.GREEN, const.LIGHT_GREEN, const.WHITE
)

# Добавляем кнопку "Сюжет"
story_button = Button(
    (const.SCREEN_WIDTH - const.BUTTON_WIDTH) // 2,
    start_y + (const.BUTTON_HEIGHT + const.BUTTON_SPACING) * 2, # Размещаем ниже new_game_button
    const.BUTTON_WIDTH,
    const.BUTTON_HEIGHT,
    "Сюжет",
    const.GRAY, const.LIGHT_GRAY, const.BLACK # Можно использовать другие цвета
)

# Текст сюжета (можно вынести в отдельный файл или константы)
STORY_TEXT = """
 Вы - одинокий зомби. Не просто ходячий мертвец, а мутировавший человек,
 бежавший из зловещих недр лаборатории "Генезис" в кишащем неоном и
 пороком Сан-Сенате. Воспоминания о прошлой жизни – обрывки: улыбка матери, 
 вкус мороженого, страх перед неизбежным – теперь лишь призраки, дразнящие 
 вас своей недостижимостью. Взамен – голод, нестерпимый, животный голод, 
 и... ярость. Ярость ко всем. К тем, кто вас создал. К тем, кто забыл.
 К тем, кто живет, когда вы – существуете.
 Ваша задача - уничтожить всех, кто вас создал.
"""

def main_menu_loop():
    global game_state, running, game_instance, screen # Объявляем screen как global, если он используется внутри

    # Состояние игры (меню, игра или сюжет)
    game_state = "menu" # 'menu', 'playing', 'story'

    # Основной цикл
    running = True
    game_instance = None # Добавлено: храним экземпляр игры здесь

    while running:
        # Проверяем, играет ли музыка, если нет - запускаем
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Если игра запущена, она сохранится сама при выходе из своего цикла
                # Если мы в меню, просто выходим
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game_state == "story":
                    game_state = "menu" # Возврат в меню по ESC

            if game_state == "menu":
                if continue_button.is_clicked(event):
                    loaded_data = save_manager.load_game()
                    if loaded_data:
                        game_instance = Game(initial_state=loaded_data)
                        game_state = "playing"

                if new_game_button.is_clicked(event):
                    game_instance = Game()
                    game_state = "playing"

                if story_button.is_clicked(event):
                    game_state = "story"

        # --- Логика отрисовки ---
        if game_state == "menu":
            if background_image:
                screen.blit(background_image, (0, 0))
            else:
                screen.fill(const.WHITE) # Резервный фон, если изображение не загрузилось
            # Обновляем состояние наведения кнопок меню
            continue_button.check_hover(mouse_pos)
            new_game_button.check_hover(mouse_pos)
            story_button.check_hover(mouse_pos) # Добавляем проверку для story_button

            # Рисуем кнопки меню
            continue_button.draw(screen)
            new_game_button.draw(screen)
            story_button.draw(screen) # Рисуем story_button

        elif game_state == "story":
            # Отрисовка экрана сюжета
            if background_image:
                screen.blit(background_image, (0, 0))
            else:
                screen.fill(const.WHITE)

            # Настройка шрифта для текста сюжета
            font = pygame.font.SysFont(None, 36)
            
            # Разбиваем текст на строки для лучшего форматирования
            lines = STORY_TEXT.strip().split('\n')
            line_height = 40  # Расстояние между строками
            
            # Вычисляем начальную позицию для отрисовки текста
            total_text_height = len(lines) * line_height
            start_y = (const.SCREEN_HEIGHT - total_text_height) // 2
            
            # Отрисовываем каждую строку текста
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, const.WHITE)  # Изменили цвет на WHITE
                text_rect = text_surface.get_rect(center=(const.SCREEN_WIDTH // 2, start_y + i * line_height))
                screen.blit(text_surface, text_rect)

            # Подсказка про ESC (тоже белым цветом)
            esc_font = pygame.font.SysFont(None, 24)
            esc_text = esc_font.render("Нажмите ESC для возврата в меню", True, const.WHITE)
            esc_rect = esc_text.get_rect(center=(const.SCREEN_WIDTH // 2, const.SCREEN_HEIGHT - 50))
            screen.blit(esc_text, esc_rect)

        elif game_state == "playing":
            if game_instance:
                # Запускаем цикл игры
                game_instance.run()
                if not game_instance.is_running: # Проверяем, хочет ли игра выйти
                    running = False # Если игра сказала выйти, выходим из цикла меню
                    break
                game_state = "menu" # Всегда возвращаемся в меню
                game_instance = None # Сбрасываем экземпляр
            else:
                # Аварийный возврат в меню, если что-то пошло не так
                game_state = "menu"

        # Обновление экрана должно быть ВНЕ условных блоков отрисовки
        pygame.display.flip()

    # Завершение Pygame и выход из приложения происходят ПОСЛЕ цикла, в main.py
    pygame.mixer.music.stop()  # Останавливаем музыку перед выходом
    pygame.quit()
    sys.exit() 

# Этот блок будет выполняться, только если menu.py запускается напрямую (для тестирования)
if __name__ == '__main__':
    main_menu_loop()
    print("Выход из приложения (menu.py).") 