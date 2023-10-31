"""
This module contains the Player class, representing a player.
"""
import chess

from src.enums import ChessColor
from src.mid_game.power_ups import PowerUp


class Player:
    """
    A player participating in the game.
    """
    name: str
    color: ChessColor
    power_ups: list[PowerUp]

    def __init__(self, name: str, color: ChessColor) -> None:
        self.name = name
        self.color = color
        self.power_ups = []

    def get_name(self) -> str:
        """
        Returns the name of the player.
        :return: The name of the player
        """
        return self.name

    def set_name(self, name: str) -> None:
        """
        Sets the name of the player.
        :param name: The new name of the player
        """
        self.name = name

    def use_powerup(self, i: int, board: chess.Board) -> None:
        """
        Uses the given power-up.
        :param board: The board on which the power-up is used
        :param i: index of the power-up to be used
        """
        if i < len(self.power_ups):
            self.power_ups[i].apply_power_up(board)

    def add_powerup(self, power_up: PowerUp) -> None:
        """
        Adds the given power-up to the player.
        :param power_up: The power-up to be added
        """
        if len(self.power_ups) < 4:
            self.power_ups.append(power_up)
