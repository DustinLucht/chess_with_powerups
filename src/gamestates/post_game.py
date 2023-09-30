"""
Game Over State
"""
import pygame

from .base import BaseState


class PostGame(BaseState):
    def __init__(self):
        super(PostGame, self).__init__()
        pass

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        pass
