"""
This module contains the ChessBoard class, representing a chess board.
"""
import chess

from src.player import Player
from src.power_up import PowerUp


class ChessBoard:
    """
    This class represents a chess board.
    """
    def __init__(self):
        self.board: chess.Board = chess.Board()
        self.current_player: Player or None = None

    def get_possible_moves(self) -> list[chess.Move]:
        """
        Returns all possible moves for the given piece.
        :return: List with all possible moves
        """
        return list(self.board.legal_moves)

    def make_move(self, move: chess.Move):
        """
        Makes the given move.
        :param move: The move to be executed
        """
        self.board.push(move)

    def apply_power_up(self, power_up: PowerUp):
        """
        Applies the given power-up.
        :param power_up: The power-up to be applied
        """
        # Implement the application of the power-up here
        pass
