import pygame
from Scripts.player import Player
import Scripts.save_manager as save_manager

class Game:
    def __init__(self, initial_state=None):
        pygame.init()
        self.screen_width = 1000
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Моя Игра")
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        if initial_state:
            print(f"--- GAME __init__: Получено initial_state: {initial_state} ---")
            print("--- GAME __init__: Вызов apply_loaded_state ---")
            save_manager.apply_loaded_state(self, initial_state)
        else:
            print("--- GAME __init__: initial_state не предоставлено, используется стандартное. ---")

    def run(self):
        while self.is_running:
            dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            if not self.is_running:
                break
            self.update(dt)
            self.render()

        print("Игровой цикл Game завершен.")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("--- GAME: Получено событие QUIT ---")
                print("--- GAME: Вызов get_game_state ---")
                current_state = save_manager.get_game_state(self)
                print(f"--- GAME: Получено состояние: {current_state} ---")
                print("--- GAME: Вызов save_manager.save_game ---")
                save_manager.save_game(current_state)
                self.is_running = False
                return

    def update(self, dt):
        self.all_sprites.update(dt)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    print("Этот файл не предназначен для прямого запуска. Запустите main.py")





