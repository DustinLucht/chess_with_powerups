"""
Game Over State
"""
import pygame

from src.enums import ChessColor
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState


class MidGameAIsTurn(MidGameBaseState):
    def __init__(self, ais_strength: float, ais_color: ChessColor):
        super(MidGameAIsTurn, self).__init__()
        # init vars
        self.ais_strength: float = ais_strength
        self.ais_color: ChessColor = ais_color

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        pass
