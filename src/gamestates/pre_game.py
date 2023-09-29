"""
PreGame state
"""
from .base import BaseState
from ..enums import GameState


class PreGame(BaseState):
    def __init__(self):
        super(PreGame, self).__init__()
        self.next_state = GameState.MID_GAME

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
