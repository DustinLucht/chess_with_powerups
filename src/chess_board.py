"""
Dieses Modul enthält die Klasse Player, die einen Spieler repräsentiert.
"""
import chess

from src.player import Player
from src.power_up import PowerUp


class ChessBoard:
    """
    Diese Klasse repräsentiert ein Schachbrett.
    """
    def __init__(self):
        self.board: chess.Board = chess.Board()
        self.current_player: Player or None = None

    def get_possible_moves(self):
        """
        Gibt alle möglichen Züge für die gegebene Figur zurück.
        :return: Liste mit allen möglichen Zügen
        """
        return list(self.board.legal_moves)

    def make_move(self, move: chess.Move):
        """
        Führt den gegebenen Zug aus.
        :param move: Der auszuführende Zug
        """
        self.board.push(move)

    def apply_power_up(self, power_up: PowerUp):
        """
        Wendet das gegebene Power-Up an.
        :param power_up: Das anzuwendende Power-Up
        """
        # Implementiere die Anwendung des Power-Ups hier
        pass
