import pygame
from Scripts.player import Player
from Scripts.vrag import EnemyManager
from Scripts.people import PeopleManager
import Scripts.save_manager as save_manager
from Scripts.button import Button
import Scripts.constant as const
import os

GAME_OVER_MUSIC = "Sprites/Player/music/game_over.mp3"
KUS_KUS = "Sprites/Player/music/kus.mp3"

class Game:
    def __init__(self, initial_state=None):
        pygame.init()
        pygame.mixer.init()
        self.screen_width = 1000
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Моя Игра")
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_game_over = False

        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        self.enemy_manager = EnemyManager(self.screen_width, self.screen_height, self.player)
        self.people_manager = PeopleManager(self.screen_width, self.screen_height)

        self.restart_button = Button(
            (self.screen_width - const.BUTTON_WIDTH) // 2,
            (self.screen_height) // 2 + 40,
            const.BUTTON_WIDTH,
            const.BUTTON_HEIGHT,
            "Сначала",
            const.GREEN, const.LIGHT_GREEN, const.WHITE
        )

        self.kus_sound = pygame.mixer.Sound(KUS_KUS)

        
        self.background_image = pygame.image.load("Sprites/Player/fon/fb9a3e4224fcec0cb837fe9927dc2fde--dungeon-tiles-deathwatch.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))
        
        self.zombie_image = pygame.image.load("Sprites/Player/fon/pngtree-cartoon-zombie-of-halloween-coming-out-of-the-broken-paper-png-image_13362557.png").convert_alpha()
        self.zombie_image = pygame.transform.smoothscale(self.zombie_image, (180, 180))
        
        self.score = 0

        if initial_state:
            save_manager.loaded_state(self, initial_state)

    def run(self):
        while self.is_running:
            dt = self.clock.tick(60) / 1000.0

            self.handle_events()
            if not self.is_running:
                break
            if not self.is_game_over:
                self.update(dt)#обновляются спрайты
                self.render()#отрисовка кадр
                self.check_collision()#проверка столкновений
            else:
                self.render_game_over()

    def handle_events(self):
        """При закрытии окна игра сохраняет состояние и завершается"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                current_state = save_manager.get_game_state(self)
                save_manager.save_game(current_state)
                self.is_running = False
                return
            if self.is_game_over:
                """Если игра завершена, проверяется наведение и клик по кнопке Сначала"""
                mouse_pos = pygame.mouse.get_pos()
                self.restart_button.check_hover(mouse_pos)
                if self.restart_button.is_clicked(event):
                    self.restart_game()

    def update(self, dt):
        self.all_sprites.update(dt)
        self.enemy_manager.update(dt)
        self.people_manager.update(dt)

    def render(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))

        score_font = pygame.font.SysFont(None, 40)
        score_surface = score_font.render(f"Счет: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (15, 10))

        self.all_sprites.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.people_manager.draw(self.screen)
        pygame.display.flip()

    def check_collision(self):
        """проверка столкновений"""
        if pygame.sprite.spritecollideany(self.player, self.enemy_manager.enemies):
            self.is_game_over = True
            self.play_game_over_music()
        collided_people = pygame.sprite.spritecollide(self.player, self.people_manager.people, False)
        for person in collided_people:
            self.people_manager.turn_person_to_bitten(person)
            self.kus_sound.play()
            self.score += 1
        if pygame.sprite.spritecollideany(self.player, self.enemy_manager.bullets):
            self.is_game_over = True
            self.play_game_over_music()

    def render_game_over(self):
        self.screen.fill(const.BLACK)
        font = pygame.font.SysFont(None, 72)
        text_surface = font.render("Вы проиграли", True, const.WHITE)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 40))
        self.screen.blit(text_surface, text_rect)
        if self.zombie_image:
            zombie_x = text_rect.right + 30
            zombie_y = text_rect.centery - self.zombie_image.get_height() // 2
            self.screen.blit(self.zombie_image, (zombie_x, zombie_y))
        self.restart_button.draw(self.screen)
        pygame.display.flip()

    def restart_game(self):
        """перезапуск игры"""
        self.is_game_over = False
        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.enemy_manager = EnemyManager(self.screen_width, self.screen_height, self.player)
        self.people_manager = PeopleManager(self.screen_width, self.screen_height)
        self.score = 0
        self.play_main_music()

    def play_main_music(self):
        pygame.mixer.music.load("Sprites/Player/music/Ghostrifter-Official-Resurgence(chosic.com).mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


    def play_game_over_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(GAME_OVER_MUSIC)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()








