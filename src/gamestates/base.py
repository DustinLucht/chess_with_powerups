"""
This module contains the base state.
"""
import pygame

from src.enums import GameState, PersistentDataKeys


class BaseState(object):
    """
    This class represents the base state.
    """
    done: bool
    quit: bool
    next_state: GameState
    screen_rect: pygame.Rect
    persist: dict[PersistentDataKeys, object]
    font: pygame.font.Font
    background_image: pygame.Surface
    background_rect: pygame.Rect

    def __init__(self) -> None:
        self.done = False
        self.quit = False
        self.next_state = GameState.MENU
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font: pygame.font.Font(None, 24)
        self.background_image = pygame.Surface(self.screen_rect.size)
        self.background_rect = self.background_image.get_rect(center=self.screen_rect.center)

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
