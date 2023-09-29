"""
This module contains the Player class, representing a player.
"""
from src.enums import ChessColor
from src.mid_game.power_up import PowerUp


class Player:
    """
    A player participating in the game.
    """
    def __init__(self, name: str, color: ChessColor):
        self.name: str = name
        self.color: ChessColor = color
        self.power_ups: list[PowerUp] = []

    def get_name(self) -> str:
        """
        Returns the name of the player.
        :return: The name of the player
        """
        return self.name

    def set_name(self, name: str):
        """
        Sets the name of the player.
        :param name: The new name of the player
        """
        self.name = name

    def use_power_up(self, power_up: PowerUp):
        """
        Uses the given power-up.
        :param power_up: The power-up to be used
        """
        # Implement the usage of the power-up here
        pass
