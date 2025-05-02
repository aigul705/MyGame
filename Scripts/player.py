import pygame
from Scripts.utils import load_sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5):
        super().__init__()
        sprite_path = "Player/player_idle/player_idle_1.png"
        try:
            self.image = load_sprite(sprite_path, with_alpha=True)
        except SystemExit:
            print(f"Не найден спрайт '{sprite_path}'. Используется зеленый квадрат.")
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.velocity = pygame.Vector2(0, 0)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.velocity.xy = (0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = 1

        # Нормализация вектора для диагонального движения
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed

        self.rect.move_ip(self.velocity * dt * 60) # Умножаем на dt и 60 для независимости от FPS

    def draw(self, surface):
        surface.blit(self.image, self.rect)
