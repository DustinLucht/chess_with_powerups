"""
Game Over State
"""
import chess
import pygame

from src.enums import ChessColor, MidGamePersistentDataKeys
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState
from src.mid_game.chess_board_gui import ChessBoardGui


class MidGameAIsTurn(MidGameBaseState):
    def __init__(self, ais_strength: float, ais_color: ChessColor, board: chess.Board, board_gui: ChessBoardGui):
        super(MidGameAIsTurn, self).__init__()
        # init vars
        self.ais_strength: float = ais_strength
        self.ais_color: ChessColor = ais_color
        self.board = board
        self.board_gui = board_gui

    def startup(self, mid_game_persistent):
        super(MidGameAIsTurn, self).startup(mid_game_persistent)
        # init board
        self.board_gui.set_figures_according_to_board()

    def get_event(self, event):
        pass

    def draw(self, surface):
        self.board_gui.draw(surface)

    def update(self, dt):
        pass
