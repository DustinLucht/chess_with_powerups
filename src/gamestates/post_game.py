"""
Game Over State
"""
import chess
import pygame

from src.gamestates.base import BaseState
from src.enums import PersistentDataKeys, GameState
from src.mid_game.chess_board_gui import ChessBoardGui


class PostGame(BaseState):
    """
    This class represents the post game.
    """
    outcome: chess.Outcome
    board_gui: ChessBoardGui

    def __init__(self):
        super(PostGame, self).__init__()
        self.outcome = chess.Outcome(chess.Termination.STALEMATE, None)
        # outcome
        self.outcome_background = pygame.Rect(0, 0, 300, 100)
        self.outcome_background.center = self.screen_rect.center
        self.outcome_background.x -= 420
        self.outcome_text = self.font.render("Unentschieden", True, pygame.Color("black"))
        self.outcome_text_rect = self.outcome_text.get_rect(center=self.outcome_background.center)
        # create "restart" and "back" buttons
        self.restart_button = pygame.Rect(0, 0, 300, 50)
        self.restart_button.center = self.screen_rect.center
        self.restart_button.y += 100
        self.restart_button.x -= 420
        self.restart_text = self.font.render("Neustart", True, pygame.Color("black"))
        self.restart_text_rect = self.restart_text.get_rect(center=self.restart_button.center)
        self.back_button = pygame.Rect(0, 0, 300, 50)
        self.back_button.center = self.screen_rect.center
        self.back_button.y += 200
        self.back_button.x -= 420
        self.back_text = self.font.render("Zurück zum Menü", True, pygame.Color("black"))
        self.back_text_rect = self.back_text.get_rect(center=self.back_button.center)

    def startup(self, persistent):
        super(PostGame, self).startup(persistent)
        # init background
        self.background_image = persistent[PersistentDataKeys.BACKGROUND_IMAGE]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)
        # init outcome
        self.outcome = persistent[PersistentDataKeys.OUTCOME]
        if self.outcome.winner == chess.WHITE:
            self.outcome_text = self.font.render("Weiß gewinnt", True, pygame.Color("black"))
        elif self.outcome.winner == chess.BLACK:
            self.outcome_text = self.font.render("Schwarz gewinnt", True, pygame.Color("black"))
        elif self.outcome.winner is None:
            self.outcome_text = self.font.render("Unentschieden", True, pygame.Color("black"))
        self.outcome_text_rect = self.outcome_text.get_rect(center=self.outcome_background.center)
        # set board gui but check type before
        if isinstance(self.persist[PersistentDataKeys.BOARD_GUI], ChessBoardGui):
            self.board_gui = self.persist[PersistentDataKeys.BOARD_GUI]
        else:
            raise TypeError("Board gui is not of type ChessBoardGui")

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button.collidepoint(mouse_pos):
                self.next_state = GameState.MID_GAME
                self.done = True
            elif self.back_button.collidepoint(mouse_pos):
                self.next_state = GameState.MENU
                self.done = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button.collidepoint(mouse_pos):
                self.restart_text = self.font.render("Neustart", True, pygame.Color("blue"))
            else:
                self.restart_text = self.font.render("Neustart", True, pygame.Color("black"))
            if self.back_button.collidepoint(mouse_pos):
                self.back_text = self.font.render("Zurück zum Menü", True, pygame.Color("blue"))
            else:
                self.back_text = self.font.render("Zurück zum Menü", True, pygame.Color("black"))

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        self.board_gui.draw(surface)
        # draw buttons
        pygame.draw.rect(surface, pygame.Color("white"), self.outcome_background)
        pygame.draw.rect(surface, pygame.Color("white"), self.restart_button)
        pygame.draw.rect(surface, pygame.Color("white"), self.back_button)
        # draw text
        surface.blit(self.outcome_text, self.outcome_text_rect)
        surface.blit(self.restart_text, self.restart_text_rect)
        surface.blit(self.back_text, self.back_text_rect)
