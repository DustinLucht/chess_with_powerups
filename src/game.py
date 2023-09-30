import pygame
import pygame_widgets

from src.enums import GameState
from src.gamestates.base import BaseState


class Game(object):
    """
    This class represents the game.
    """
    def __init__(self, screen, states, start_state) -> None:
        self.done: bool = False
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.fps: int = 60
        self.states: dict[GameState, BaseState] = states
        self.state_name = start_state
        self.state: BaseState = self.states[self.state_name]

    def event_loop(self) -> None:
        """
        Handles events.
        :return: None
        """
        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            self.state.get_event(event)

    def flip_state(self) -> None:
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

    def update(self, dt) -> None:
        """
        Updates the game.
        :param dt:
        :return: None
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self) -> None:
        """
        Draws the game.
        :return: None
        """
        self.state.draw(self.screen)

    def run(self) -> None:
        """
        Runs the game.
        :return: None
        """
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()
