import pygame
from Scripts.utils import load_sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, scale_factor=0.1):
        super().__init__()
        sprite_path = "Player/player_idle/player_idle_1.png"
        original_image_loaded = None
        try:
            original_image_loaded = load_sprite(sprite_path, with_alpha=True)
        except SystemExit:
            print(f"Не найден спрайт '{sprite_path}'. Используется зеленый квадрат.")
            original_image_loaded = pygame.Surface((50, 50))
            original_image_loaded.fill((0, 255, 0))

        if original_image_loaded:
            original_width, original_height = original_image_loaded.get_size()
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            self.original_scaled_image = pygame.transform.scale(original_image_loaded, (new_width, new_height))
        else:
            print("Ошибка: Не удалось загрузить/создать исходное изображение.")
            self.original_scaled_image = pygame.Surface((int(50 * scale_factor), int(50 * scale_factor)))
            self.original_scaled_image.fill((255, 0, 0))

        self.image = self.original_scaled_image
        self.facing_right = False
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

        is_moving_right = self.velocity.x > 0
        is_moving_left = self.velocity.x < 0

        if is_moving_right and not self.facing_right:
            self.image = pygame.transform.flip(self.original_scaled_image, True, False)
            self.facing_right = True
        elif is_moving_left and self.facing_right:
            self.image = self.original_scaled_image
            self.facing_right = False

        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed

        self.rect.move_ip(self.velocity * dt * 60)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
