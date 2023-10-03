"""
Game Over State
"""
import pygame

from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState


class MidGamePause(MidGameBaseState):
    def __init__(self):
        super(MidGamePause, self).__init__()
        pass

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        pass