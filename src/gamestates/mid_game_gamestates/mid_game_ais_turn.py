"""
Game Over State
"""
import chess

from src.enums import ChessColor
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState
from src.mid_game.chess_board_gui import ChessBoardGui


class MidGameAIsTurn(MidGameBaseState):
    """
    This class represents the post game.
    """
    ais_strength: float

    def __init__(self, color: ChessColor, ais_strength: float, board: chess.Board, board_gui: ChessBoardGui):
        super(MidGameAIsTurn, self).__init__(color)
        # init vars
        self.ais_strength = ais_strength
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
