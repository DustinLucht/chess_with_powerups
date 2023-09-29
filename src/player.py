"""
Dieses Modul enthält die Klasse Player, die einen Spieler repräsentiert.
"""
from src.enums import ChessColor
from src.power_up import PowerUp


class Player:
    """
    Ein Spieler, der am Spiel teilnimmt.
    """
    def __init__(self, name: str, color: ChessColor):
        self.name: str = name
        self.color: ChessColor = color
        self.power_ups: list[PowerUp] = []

    def get_name(self):
        """
        Gibt den Namen des Spielers zurück.
        :return: Den Namen des Spielers
        """
        return self.name

    def set_name(self, name):
        """
        Setzt den Namen des Spielers.
        :param name: Der neue Name des Spielers
        """
        self.name = name

    def use_power_up(self, power_up):
        """
        Verwendet das gegebene Power-Up.
        :param power_up: Das zu verwendende Power-Up
        """
        # Implementiere die Verwendung des Power-Ups hier
        pass
