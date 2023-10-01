"""
Game Over State
"""
import pygame

from src.enums import ChessColor, MidGamePersistentDataKeys
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState


class MidGameAIsTurn(MidGameBaseState):
    def __init__(self, ais_strength: float, ais_color: ChessColor):
        super(MidGameAIsTurn, self).__init__()
        # init vars
        self.ais_strength: float = ais_strength
        self.ais_color: ChessColor = ais_color

    def startup(self, mid_game_persistent):
        super(MidGameAIsTurn, self).startup(mid_game_persistent)
        # init board
        self.board = mid_game_persistent[MidGamePersistentDataKeys.BOARD]
        self.board_gui = mid_game_persistent[MidGamePersistentDataKeys.BOARD_GUI]
        self.board_gui.set_figures_according_to_board(self.board)
        # init background
        self.background_image = mid_game_persistent[MidGamePersistentDataKeys.BACKGROUND_IMAGE]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        pass

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        self.board_gui.draw_chessboard(surface)
        self.board_gui.draw_figures(surface)

    def update(self, dt):
        pass
