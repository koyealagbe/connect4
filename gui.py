"""
gui.py
Contains classes for graphical elements
"""

import pygame

class Text:
    def __init__(self, text, font_name, font_size, font_color):
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = text
        self.font_color = font_color
        self.obj = self.font.render(self.text, True, self.font_color)
        self.rect = self.obj.get_rect()

    # Place the center of the text at (x, y)
    def position_center(self, x, y):
        self.rect.center = (x, y)
    
    # Place the top left corner of the text at (x, y)
    def position_topleft(self, x, y):
        self.rect.topleft = (x, y)

    def set_text(self, text, color=None):
        self.obj = self.font.render(text, True, self.font_color if color == None else color)
        self.rect = self.obj.get_rect()

class Button:
    def __init__(self, x, y, width, height, bg_color, text, font_name, font_size, font_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text = Text(text, font_name, font_size, font_color)
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.text.position_center(self.width // 2, self.height // 2)

    def draw(self, display):
        self.surf.fill(self.bg_color)
        self.surf.blit(self.text.obj, self.text.rect)
        display.blit(self.surf, self.rect)

    def is_hovering(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

class Circle: 
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)
    
    def draw(self, surf, color):
        pygame.draw.circle(surf, color, (self.x + self.radius, self.y + self.radius), self.radius)
    
    def is_hovering(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
