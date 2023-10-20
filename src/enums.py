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


class MidGameState(Enum):
    """Enum for the different states of the mid game."""
    PLAYERS_1_TURN = 0
    PLAYERS_2_TURN = 1
    PAUSE = 2


class PersistentDataKeys(Enum):
    """Enum for the different keys of the persistent data."""
    BACKGROUND_IMAGE = 0
    SINGLE_PLAYER = 1
    STARTS_WITH_WHITE = 2
    DIFFICULTY = 3
    POWER_UP_MULTIPLICATOR = 4
    OUTCOME = 5
    BOARD_GUI = 6


class MidGamePersistentDataKeys(Enum):
    """Enum for the different keys of the persistent data."""
    CURRENT_TURN = 0
    DRAW_OFFERED = 1
    DRAW_ACCEPTED = 2
    FORFEIT = 3
    RESTART = 4


class OverlayType(Enum):
    """Enum for the different types of overlays."""
    SELECTED_FIGURE = 0
    POSSIBLE_MOVE_NORMAL = 1
    POSSIBLE_MOVE_ATTACK = 2
    PROMOTION_QUEEN = 3
    PROMOTION_ROOK = 4
    PROMOTION_BISHOP = 5
    PROMOTION_KNIGHT = 6


class ChessColor(Enum):
    """Enum for the different colors of the chess pieces."""
    BLACK = False
    WHITE = True


class PowerUpTypes(Enum):
    """Enum for the different types of power-ups."""
    FREEZE = 1
    DOUBLE_MOVE = 2
