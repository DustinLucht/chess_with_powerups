"""
This module contains the base state.
"""
import pygame

from src.enums import GameState


class BaseState(object):
    """
    This class represents the base state.
    """
    def __init__(self) -> None:
        self.done: bool = False
        self.quit: bool = False
        self.next_state: GameState = GameState.MENU
        self.screen_rect: pygame.Rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font: pygame.font.Font = pygame.font.Font(None, 24)

    def startup(self, persistent: dict) -> None:
        """
        Starts up the state.
        :param persistent: persistent data
        """
        self.persist = persistent

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
