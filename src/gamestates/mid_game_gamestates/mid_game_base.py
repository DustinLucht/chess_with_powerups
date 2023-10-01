"""
This module contains the base state.
"""
import pygame

from src.enums import MidGamePersistentDataKeys, MidGameState


class MidGameBaseState(object):
    """
    This class represents the base state.
    """
    def __init__(self) -> None:
        self.done: bool = False
        self.quit: bool = False
        self.next_state: MidGameState = MidGameState.PAUSE
        self.screen_rect: pygame.Rect = pygame.display.get_surface().get_rect()
        self.mid_game_persist: dict[MidGamePersistentDataKeys, object] = {}
        self.font: pygame.font.Font = pygame.font.Font(None, 24)

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
