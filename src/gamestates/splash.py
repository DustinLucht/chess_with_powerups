"""
This module contains the Splash class.
"""
import pygame
from ..gamestates.base import BaseState
from ..enums import GameState, PersistentDataKeys


class Splash(BaseState):
    """
    This class represents the splash screen.
    """
    time_active: int
    current_alpha: int

    def __init__(self):
        super(Splash, self).__init__()
        self.next_state = GameState.MENU
        self.time_active = 0
        self.background_image = pygame.image.load("assets\\images\\board\\gr-stocks-Iq9SaJezkOE-unsplash.jpg")
        self.current_alpha = 0
        self.background_image = pygame.transform.scale(self.background_image, self.screen_rect.size)
        self.background_rect = self.background_image.get_rect(center=self.screen_rect.center)

    def update(self, dt):
        self.time_active += dt
        if self.time_active >= 500:
            self.persist[PersistentDataKeys.BACKGROUND_IMAGE] = self.background_image
            self.done = True
        self.current_alpha = max(0, int((self.time_active / 5000) * 255))
        self.background_image.set_alpha(self.current_alpha)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
