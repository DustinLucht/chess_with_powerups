import pygame
import pygame_widgets

from src.enums import GameState
from src.gamestates.base import BaseState


class Game:
    """
    This class represents the game.
    """
    done: bool
    screen: pygame.Surface
    clock: pygame.time.Clock
    fps: int
    states: dict[GameState, BaseState]
    state_name: GameState
    state: BaseState

    def __init__(self, screen: pygame.Surface, states: dict[GameState, BaseState], start_state: GameState) -> None:
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def run(self) -> None:
        """
        Runs the game.
        :return: None
        """
        while not self.done:
            dt = self.clock.tick(self.fps)
            self._event_loop()
            self._update(dt)
            self._draw()
            pygame.display.update()

    def _event_loop(self) -> None:
        """
        Handles events.
        :return: None
        """
        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            self.state.get_event(event)

    def _flip_state(self) -> None:
        """
        Flips the state.
        :return: None
        """
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def _update(self, dt: int) -> None:
        """
        Updates the game.
        :param dt:
        :return: None
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self._flip_state()
        self.state.update(dt)

    def _draw(self) -> None:
        """
        Draws the game.
        :return: None
        """
        self.state.draw(self.screen)

