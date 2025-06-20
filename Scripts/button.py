import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font_size=30):
        """инициализация кнопки с определёнными параметрами: координаты, текст, цвет и тд"""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)#шрифт по умолч
        self.is_hovered = False #курсор

    def check_hover(self, mouse_pos):
        """координаты курсора внутри кнопки"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)#коорд курсора

    def is_clicked(self, event):
        """Функция провекрки клика левой мышки по кнопке
         args: событие - курсор внутри кнопки, клик левой
        return: да или нет """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #клик левой
            if self.rect.collidepoint(event.pos):# внутри кнопки
                return True
        return False

    def draw(self, surface):
        """отрисовка кнопки нужного цвета, текста и тд"""
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=5)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)



 