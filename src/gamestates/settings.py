"""
Settings game state
"""
import pygame

from src.gamestates.base import BaseState
from src.enums import GameState, PersistentDataKeys


class Settings(BaseState):
    """
    This class represents the settings.
    """
    def __init__(self):
        super(Settings, self).__init__()
        # back button
        self.back_button = pygame.Rect(0, 0, 300, 50)
        self.back_button.center = self.screen_rect.center
        self.back_button.y += 100
        # draw text
        self.back_text = self.font.render("Zurück", True, pygame.Color("black"))
        self.back_text_rect = self.back_text.get_rect(center=self.back_button.center)

    def startup(self, persistent):
        super(Settings, self).startup(persistent)
        self.background_image = persistent[PersistentDataKeys.BACKGROUND_IMAGE]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)
        self.next_state = GameState.MENU

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.back_button.collidepoint(mouse_pos):
                self.done = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if self.back_button.collidepoint(mouse_pos):
                self.back_text = self.font.render("Zurück", True, pygame.Color("blue"))
            else:
                self.back_text = self.font.render("Zurück", True, pygame.Color("black"))

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        # draw back button
        pygame.draw.rect(surface, pygame.Color("white"), self.back_button)
        surface.blit(self.back_text, self.back_text_rect)
