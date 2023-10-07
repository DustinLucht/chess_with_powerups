"""
This module contains the base state.
"""
import chess
import pygame

from src.enums import MidGamePersistentDataKeys, MidGameState, ChessColor
from src.mid_game.chess_board_gui import ChessBoardGui


class MidGameBaseState(object):
    """
    This class represents the base state.
    """
    def __init__(self, color: ChessColor) -> None:
        self.done: bool = False
        self.quit: bool = False
        self.next_state: MidGameState = MidGameState.PAUSE
        self.screen_rect: pygame.Rect = pygame.display.get_surface().get_rect()
        self.mid_game_persist: dict[MidGamePersistentDataKeys, object] = {}
        self.font: pygame.font.Font = pygame.font.Font(None, 24)
        # init board
        self.board: chess.Board = chess.Board()
        self.board_gui: ChessBoardGui = ChessBoardGui(self.board, 0, 0)
        # init background
        self.background_image: pygame.Surface = pygame.Surface(self.screen_rect.size)
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)
        # vars
        self.color: ChessColor = color

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
