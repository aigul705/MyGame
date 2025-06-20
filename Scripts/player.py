import pygame
from Scripts.utils import load_sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5, scale_factor=0.1):
        """инициализация игрока: размеры, скорость, взгляд ..."""
        super().__init__()
        sprite_path = "Player/player_idle/player_idle_1.png"
        orig_ima = load_sprite(sprite_path, with_alpha=True)

        
        original_width, original_height = orig_ima.get_size()
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self.orig_scal = pygame.transform.scale(orig_ima, (new_width, new_height))
       

        self.image = self.orig_scal
        self.facing_right = False #взгляд игрока
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.velocity = pygame.Vector2(0, 0) #вектор скорости

    def update(self, dt):
        keys = pygame.key.get_pressed()#True, если клавиша нажата
        self.velocity.xy = (0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = 1

        moving_right = self.velocity.x > 0
        moving_left = self.velocity.x < 0
        #поворот картинки
        if moving_right and not self.facing_right:
            self.image = pygame.transform.flip(self.orig_scal, True, False)
            self.facing_right = True
        elif moving_left and self.facing_right:
            self.image = self.orig_scal
            self.facing_right = False
        #нормализация скорости
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed

        self.rect.move_ip(self.velocity * dt * 60) #перемещение на заданный вектор

    def draw(self, surface):
        surface.blit(self.image, self.rect)
