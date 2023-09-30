import pygame
from .base import BaseState
from ..enums import GameState


class Splash(BaseState):
    def __init__(self):
        super(Splash, self).__init__()
        self.next_state: GameState = GameState.MENU
        self.time_active: int = 0
        self.background_image: pygame.Surface = pygame.image.load(
            "..\\assets\\images\\board\\gr-stocks-Iq9SaJezkOE-unsplash.jpg")
        self.current_alpha: float = 0.0
        self.background_image = pygame.transform.scale(self.background_image, self.screen_rect.size)
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

    def update(self, dt):
        self.time_active += dt
        if self.time_active >= 500:
            self.persist["background_image"] = self.background_image
            self.done = True
        self.current_alpha = max(0, int((self.time_active / 5000) * 255))
        self.background_image.set_alpha(self.current_alpha)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
