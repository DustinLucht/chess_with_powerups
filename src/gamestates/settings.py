"""
Settings game state
"""
from .base import BaseState
from ..enums import GameState


class Settings(BaseState):
    def __init__(self):
        super(Settings, self).__init__()
        self.next_state = GameState.MENU

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
