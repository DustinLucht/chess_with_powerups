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

    def __init__(self, screen, states, start_state) -> None:
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

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
