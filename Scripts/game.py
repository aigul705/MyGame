import pygame
from Scripts.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Моя Игра")
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def run(self):
        while self.is_running:
            dt = self.clock.tick(60) / 1000.0 # Дельта времени в секундах

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            # Дополнительная обработка событий может быть здесь

    def update(self, dt):
        self.all_sprites.update(dt)
        # Логика обновления других игровых объектов

    def render(self):
        self.screen.fill((0, 0, 255)) # Синий фон
        self.all_sprites.draw(self.screen) # Используем draw группы спрайтов
        pygame.display.flip()

if __name__ == '__main__':
    print("Этот файл не предназначен для прямого запуска. Запустите main.py")





