"""
MidGame class
"""
import pygame
import chess
from .base import BaseState
from ..mid_game.chess_board_gui import ChessBoardGui

SQUARE_SIZE = 120


class MidGame(BaseState):
    def __init__(self):
        super(MidGame, self).__init__()
        self.board: chess.Board = chess.Board()
        self.board_gui: ChessBoardGui = ChessBoardGui(SQUARE_SIZE)
        self.background_image: pygame.Surface = pygame.Surface(self.screen_rect.size)
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

    def startup(self, persistent):
        super(MidGame, self).startup(persistent)
        self.board = chess.Board()
        self.background_image = persistent["background_image"]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            print(self.board_gui.get_correlating_square_id_or_none(event.pos))
            print(self.board_gui.get_square_coordinates(self.board_gui.get_correlating_square_id_or_none(event.pos)))

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        self.board_gui.draw_chessboard(surface)
        self.board_gui.draw_figures(surface, self.board)

    def update(self, dt):
        pass
