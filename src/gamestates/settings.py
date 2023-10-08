"""
Settings game state
"""
import pygame

from base import BaseState
from ..enums import GameState


class Settings(BaseState):
    """
    This class represents the settings.
    """
    def __init__(self):
        super(Settings, self).__init__()
        self.next_state = GameState.MENU

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        pass
