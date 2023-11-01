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

    def get_powerup(self, i: int) -> PowerUp:
        """
        Returns the power-up at the given index.
        :param i: index of the power-up
        :return: The power-up at the given index
        """
        return self.power_ups[i]

    def get_powerups(self) -> list[PowerUp]:
        """
        Returns all power-ups of the player.
        :return: All power-ups of the player
        """
        return self.power_ups

    def set_name(self, name: str) -> None:
        """
        Sets the name of the player.
        :param name: The new name of the player
        """
        self.name = name

    def use_powerup(self, i: int) -> None:
        """
        Uses the given power-up.
        :param i: index of the power-up to be used
        """
        del self.power_ups[i]

    def add_powerup(self, power_up: PowerUp | None) -> None:
        """
        Adds the given power-up to the player.
        :param power_up: The power-up to be added
        """
        if len(self.power_ups) < 4:
            if power_up is not None:
                self.power_ups.append(power_up)
