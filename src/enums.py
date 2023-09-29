"""
This module contains the enums used in the game.
"""
from enum import Enum


class GameState(Enum):
    """Enum for the different states of the game."""
    SPLASH = 0
    MENU = 1
    SETTINGS = 2
    PRE_GAME = 3
    MID_GAME = 4
    PAUSE = 5
    POST_GAME = 6


class ChessColor(Enum):
    """Enum for the different colors of the chess pieces."""
    BLACK = 1
    WHITE = 2


class PowerUpTypes(Enum):
    """Enum for the different types of power-ups."""
    FREEZE = 1
    DOUBLE_MOVE = 2
