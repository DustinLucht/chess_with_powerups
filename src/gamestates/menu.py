"""
Menu game state
"""
import pygame
from src.gamestates.base import BaseState
from src.enums import GameState, PersistentDataKeys


class Menu(BaseState):
    """
    This class represents the menu.
    """
    active_index: int
    options: dict[int, str]

    def __init__(self):
        super(Menu, self).__init__()
        self.active_index = 0
        self.next_state = GameState.PRE_GAME
        self.font = pygame.font.Font(None, 45)
        self.start_button = pygame.Rect(0, 0, 300, 50)
        self.start_button.center = self.screen_rect.center
        self.start_button.y -= 100
        self.quit_button = pygame.Rect(0, 0, 300, 50)
        self.quit_button.center = self.screen_rect.center
        self.quit_button.y += 100
        # draw text
        self.start_text = self.font.render("Start", True, pygame.Color("black"))
        self.start_text_rect = self.start_text.get_rect(center=self.start_button.center)
        self.quit_text = self.font.render("Beenden", True, pygame.Color("black"))
        self.quit_text_rect = self.quit_text.get_rect(center=self.quit_button.center)

    def startup(self, persistent):
        super(Menu, self).startup(persistent)
        self.background_image = persistent[PersistentDataKeys.BACKGROUND_IMAGE]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)
        self.next_state = GameState.PRE_GAME

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button.collidepoint(mouse_pos):
                self.next_state = GameState.PRE_GAME
                self.done = True
            elif self.quit_button.collidepoint(mouse_pos):
                self.quit = True
        # check if mouse is hovering over a button and change color
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button.collidepoint(mouse_pos):
                self.start_text = self.font.render("Start", True, pygame.Color("blue"))
            else:
                self.start_text = self.font.render("Start", True, pygame.Color("black"))
            if self.quit_button.collidepoint(mouse_pos):
                self.quit_text = self.font.render("Beenden", True, pygame.Color("blue"))
            else:
                self.quit_text = self.font.render("Beenden", True, pygame.Color("black"))

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        # draw buttons
        pygame.draw.rect(surface, pygame.Color("white"), self.start_button)
        pygame.draw.rect(surface, pygame.Color("white"), self.quit_button)
        surface.blit(self.start_text, self.start_text_rect)
        surface.blit(self.quit_text, self.quit_text_rect)
