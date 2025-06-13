import pygame
import random
import time
from Scripts.utils import load_sprite
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, player):
        super().__init__()
        # Загружаем и уменьшаем спрайт врага в 10 раз
        original_image = load_sprite("Player/vrag/9829a9e2541f7d093f6b57cef05c5902.png", with_alpha=True)
        scale_factor = 0.1
        new_width = int(original_image.get_width() * scale_factor)
        new_height = int(original_image.get_height() * scale_factor)
        self.original_image = pygame.transform.scale(original_image, (new_width, new_height))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        # Генерируем случайную позицию в пределах экрана
        max_x = max(0, screen_width - self.rect.width)
        max_y = max(0, screen_height - self.rect.height)
        self.rect.x = random.randint(0, max_x)
        self.rect.y = random.randint(0, max_y)
        
        # Сохраняем ссылку на игрока
        self.player = player
        self.facing_right = True

        # Время создания врага
        self.creation_time = time.time()
        # Время жизни врага (3 секунды)
        self.lifetime = 3

    def update(self, dt):
        # Поворот врага в зависимости от положения игрока
        if self.player:
            if self.player.rect.centerx > self.rect.centerx and not self.facing_right:
                self.image = pygame.transform.flip(self.original_image, True, False)
                self.facing_right = True
            elif self.player.rect.centerx < self.rect.centerx and self.facing_right:
                self.image = self.original_image
                self.facing_right = False
        # Проверяем, не истекло ли время жизни врага
        if time.time() - self.creation_time > self.lifetime:
            self.kill()  # Удаляем врага, если время истекло

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, speed=200):
        super().__init__()
        self.image = pygame.Surface((10, 4), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 220, 0), (0, 0, 10, 4))
        # Поворачиваем пулю по направлению
        dx, dy = target_pos[0] - start_pos[0], target_pos[1] - start_pos[1]
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=start_pos)
        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        self.velocity = (dx / length * speed, dy / length * speed)

    def update(self, dt):
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt
        # Удаляем пулю, если она вышла за экран
        if (self.rect.right < 0 or self.rect.left > 1200 or
            self.rect.bottom < 0 or self.rect.top > 800):
            self.kill()

class EnemyManager:
    def __init__(self, screen_width, screen_height, player):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player = player
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()  # Группа пуль
        self.last_wave_time = time.time()
        self.wave_interval = 5  # Интервал между волнами (сек)
        self.wave_active = False

    def update(self, dt):
        current_time = time.time()
        # Если нет врагов на экране и прошло достаточно времени — запускаем новую волну
        if not self.enemies and (current_time - self.last_wave_time >= self.wave_interval):
            self.spawn_wave()
            self.last_wave_time = current_time
        self.enemies.update(dt)
        self.bullets.update(dt)

    def spawn_wave(self):
        num_enemies = random.randint(1, 5)
        for _ in range(num_enemies):
            enemy = Enemy(self.screen_width, self.screen_height, self.player)
            self.enemies.add(enemy)
            # Создаем пулю для каждого врага
            bullet = Bullet(enemy.rect.center, self.player.rect.center)
            self.bullets.add(bullet)

    def draw(self, screen):
        # Отрисовываем всех врагов
        self.enemies.draw(screen)
        # Отрисовываем пули
        self.bullets.draw(screen) 