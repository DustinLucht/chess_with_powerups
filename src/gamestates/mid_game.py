"""
MidGame class
"""
import pygame

from .base import BaseState


class MidGame(BaseState):
    def __init__(self):
        super(MidGame, self).__init__()
        pass

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        pass
