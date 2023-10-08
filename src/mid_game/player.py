"""
This module contains the Player class, representing a player.
"""
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

    def use_power_up(self, power_up: PowerUp) -> None:
        """
        Uses the given power-up.
        :param power_up: The power-up to be used
        """
        # Implement the usage of the power-up here
        pass
