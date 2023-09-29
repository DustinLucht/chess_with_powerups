"""
This module contains the enums used in the game.
"""
from enum import Enum


class GameState(Enum):
    """Enum for the different states of the game."""
    MENU = 0
    SETTINGS = 1
    PRE_GAME = 2
    MID_GAME = 3
    PAUSE = 4
    GAME_OVER = 5

class ChessColor(Enum):
    """Enum for the different colors of the chess pieces."""
    BLACK = 1
    WHITE = 2

class PowerUpTypes(Enum):
    """Enum for the different types of power-ups."""
    FREEZE = 1
    DOUBLE_MOVE = 2
