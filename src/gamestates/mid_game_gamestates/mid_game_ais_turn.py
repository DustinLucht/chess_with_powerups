"""
Game Over State
"""
import chess
import pygame

from src.enums import ChessColor
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState
from src.mid_game.chess_board_gui import ChessBoardGui


class MidGameAIsTurn(MidGameBaseState):
    def __init__(self, ais_strength: float, ais_color: ChessColor):
        super(MidGameAIsTurn, self).__init__()
        # init board
        self.board: chess.Board = chess.Board()
        self.board_gui: ChessBoardGui = ChessBoardGui(self.board, 0, 0)
        # init vars
        self.ais_strength: float = ais_strength
        self.ais_color: ChessColor = ais_color
        # init background
        self.background_image: pygame.Surface = pygame.Surface(self.screen_rect.size)
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        pass
