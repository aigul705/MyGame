import pygame
import random
import time
from Scripts.utils import load_sprite

PEOPLE_IMAGES = [
    ("Player/people/3368686-middle.png", 0.15),
    ("Player/people/4132257-middle.png", 0.07),
    ("Player/people/1617088568_51556.png", 0.15),
    ("Player/people/fa05a412-468d-489f-a6fd-693a10d86f98.png", 0.15)
]
BITTEN_IMAGES = [
    "Player/player_idle/3ff9e1509db139577928448ffbde8810.png",
    "Player/player_idle/d837ec867953a282721c18b50337ae38.png",
    "Player/player_idle/dfb71789a47c71c7665fc241c0a6ab3c.png"
]

class Person(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, pos=None, image_path=None, scale_factor=None, creation_time=None, lifetime=None):
        super().__init__()
        if image_path is None or scale_factor is None:
            self.image_path, self.scale_factor = random.choice(PEOPLE_IMAGES)
        else:
            self.image_path = image_path
            self.scale_factor = scale_factor
        original_image = load_sprite(self.image_path, with_alpha=True)
        new_width = int(original_image.get_width() * self.scale_factor)
        new_height = int(original_image.get_height() * self.scale_factor)
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()
        if pos is not None:
            self.rect.center = tuple(pos)
        else:
            max_x = max(0, screen_width - self.rect.width)
            max_y = max(0, screen_height - self.rect.height)
            self.rect.x = random.randint(0, max_x)
            self.rect.y = random.randint(0, max_y)
        self.creation_time = creation_time if creation_time is not None else time.time()
        self.lifetime = lifetime if lifetime is not None else 5

    def update(self, dt):
        if time.time() - self.creation_time > self.lifetime:
            self.kill()

class BittenZombie(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, remaining_lifetime, image_path=None, creation_time=None):
        super().__init__()
        if image_path is None:
            import random
            from Scripts.people import BITTEN_IMAGES
            image_path = random.choice(BITTEN_IMAGES)
        self.image_path = image_path
        from Scripts.utils import load_sprite
        original_image = load_sprite(self.image_path, with_alpha=True)
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.creation_time = creation_time if creation_time is not None else time.time()
        self.lifetime = remaining_lifetime

    def update(self, dt):
        if time.time() - self.creation_time > self.lifetime:
            self.kill()

class PeopleManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.people = pygame.sprite.Group()
        self.bitten_zombies = pygame.sprite.Group()
        self.last_wave_time = time.time()
        self.wave_interval = 4

    def update(self, dt):
        current_time = time.time()
        if not self.people and (current_time - self.last_wave_time >= self.wave_interval):
            self.spawn_wave()
            self.last_wave_time = current_time
        self.people.update(dt)
        self.bitten_zombies.update(dt)

    def spawn_wave(self):
        num_people = random.randint(1, 3)
        for _ in range(num_people):
            person = Person(self.screen_width, self.screen_height)
            self.people.add(person)

    def draw(self, screen):
        self.people.draw(screen)
        self.bitten_zombies.draw(screen)

    def turn_person_to_bitten(self, person):
        elapsed = time.time() - person.creation_time
        remaining_lifetime = max(0.1, person.lifetime - elapsed)
        bitten = BittenZombie(person.rect.x, person.rect.y, person.rect.width, person.rect.height, remaining_lifetime)
        self.bitten_zombies.add(bitten)
        person.kill() 