"""
This module contains the base state.
"""
import chess
import pygame

from src.enums import MidGamePersistentDataKeys, MidGameState, ChessColor
from src.mid_game.chess_board_gui import ChessBoardGui
from src.mid_game.player import Player
from src.mid_game.power_ups import PowerUp


class MidGameBaseState(object):
    """
    This class represents the base state.
    """
    done: bool
    quit: bool
    next_state: MidGameState
    screen_rect: pygame.Rect
    mid_game_persist: dict[MidGamePersistentDataKeys, object]
    font: pygame.font.Font
    board: chess.Board
    board_gui: ChessBoardGui
    background_image: pygame.Surface
    background_rect: pygame.Rect
    color: ChessColor
    active_powerup: PowerUp | None

    def __init__(self, color: ChessColor) -> None:
        self.done = False
        self.quit = False
        self.next_state = MidGameState.PAUSE
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.mid_game_persist = {}
        self.font = pygame.font.Font(None, 24)
        # init board
        self.board = chess.Board()
        self.board_gui = ChessBoardGui(self.board, 0, 0)
        # init background
        self.background_image = pygame.Surface(self.screen_rect.size)
        self.background_rect = self.background_image.get_rect(center=self.screen_rect.center)
        # vars
        self.color = color
        self.active_powerup = None

    def startup(self, mid_game_persistent: dict) -> None:
        """
        Starts up the state.
        :param mid_game_persistent: mid_game_persistent data
        """
        self.mid_game_persist = mid_game_persistent

    def get_event(self, event: pygame.event.Event) -> None:
        """
        Gets an event.
        :param event: event
        """
        pass

    def update(self, dt: int) -> None:
        """
        Updates the state.
        :param dt: delta time
        """
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the state.
        :param surface: surface
        """
        pass

    def get_player_or_none(self) -> Player | None:
        """
        Gets the player or none.
        :return: None
        """
        return None

    def activate_powerup(self, powerup: PowerUp) -> None:
        """
        Activates the powerup.
        :param powerup: powerup
        """
        self.active_powerup = powerup
