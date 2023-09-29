"""
Game Over State
"""
from .base import BaseState


class PostGame(BaseState):
    def __init__(self):
        super(PostGame, self).__init__()
        pass

    def get_event(self, event):
        pass

    def draw(self, surface):
        pass
