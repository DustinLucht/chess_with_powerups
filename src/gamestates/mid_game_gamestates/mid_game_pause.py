"""
Game Over State
"""
import pygame

from src.enums import MidGamePersistentDataKeys
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState


class MidGamePause(MidGameBaseState):
    """
    This class represents the post game.
    """
    def __init__(self, color):
        super(MidGamePause, self).__init__(color)
        # create "resume", "restart" and "quit" buttons
        self.resume_button = pygame.Rect(0, 0, 200, 50)
        self.resume_button.center = self.screen_rect.center
        self.resume_button.y -= 100
        self.restart_button = pygame.Rect(0, 0, 200, 50)
        self.restart_button.center = self.screen_rect.center
        self.quit_button = pygame.Rect(0, 0, 200, 50)
        self.quit_button.center = self.screen_rect.center
        self.quit_button.y += 100
        # draw text
        self.resume_text = self.font.render("Weiter", True, pygame.Color("black"))
        self.resume_text_rect = self.resume_text.get_rect(center=self.resume_button.center)
        self.restart_text = self.font.render("Neustart", True, pygame.Color("black"))
        self.restart_text_rect = self.restart_text.get_rect(center=self.restart_button.center)
        self.quit_text = self.font.render("Beenden", True, pygame.Color("black"))
        self.quit_text_rect = self.quit_text.get_rect(center=self.quit_button.center)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.resume_button.collidepoint(mouse_pos):
                self.done = True
            elif self.restart_button.collidepoint(mouse_pos):
                self.mid_game_persist[MidGamePersistentDataKeys.RESTART] = True
                self.done = True
            elif self.quit_button.collidepoint(mouse_pos):
                self.quit = True
        # check if mouse is hovering over a button and change color
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if self.resume_button.collidepoint(mouse_pos):
                self.resume_text = self.font.render("Weiter", True, pygame.Color("blue"))
            else:
                self.resume_text = self.font.render("Weiter", True, pygame.Color("black"))
            if self.restart_button.collidepoint(mouse_pos):
                self.restart_text = self.font.render("Neustart", True, pygame.Color("blue"))
            else:
                self.restart_text = self.font.render("Neustart", True, pygame.Color("black"))
            if self.quit_button.collidepoint(mouse_pos):
                self.quit_text = self.font.render("Beenden", True, pygame.Color("blue"))
            else:
                self.quit_text = self.font.render("Beenden", True, pygame.Color("black"))

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        # draw buttons
        pygame.draw.rect(surface, pygame.Color("white"), self.resume_button)
        pygame.draw.rect(surface, pygame.Color("white"), self.restart_button)
        pygame.draw.rect(surface, pygame.Color("white"), self.quit_button)
        surface.blit(self.resume_text, self.resume_text_rect)
        surface.blit(self.restart_text, self.restart_text_rect)
        surface.blit(self.quit_text, self.quit_text_rect)
