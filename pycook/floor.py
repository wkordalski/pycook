import pygame


class SolidColor:
    def __init__(self, color, rect):
        self.color = color
        self.rect = rect

    def draw(self, engine):
        pygame.draw.rect(
            engine.screen, self.color, pygame.Rect(*self.rect), 3
        )
