"""
MidGame class
"""
import pygame
import chess
from .base import BaseState
from ..mid_game.chess_board_gui import ChessBoardGui

SQUARE_SIZE = 120
PIECES_SIZE = 0.7


class MidGame(BaseState):
    def __init__(self):
        super(MidGame, self).__init__()
        self.is_figure_dragging: bool = False
        self.id_figure_dragging: int = 0
        self.players_turn: bool = True
        self.board: chess.Board = chess.Board()
        self.board_gui: ChessBoardGui = ChessBoardGui(self.board, SQUARE_SIZE, PIECES_SIZE)
        self.background_image: pygame.Surface = pygame.Surface(self.screen_rect.size)
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

    def startup(self, persistent):
        super(MidGame, self).startup(persistent)
        self.board = chess.Board()
        self.background_image = persistent["background_image"]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)
        self.board_gui.set_figures_according_to_board(self.board)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                square_id = self.board_gui.get_correlating_square_id_or_none(event.pos)
                if square_id is not None:
                    self.is_figure_dragging = True
                    self.id_figure_dragging = square_id
                    figure = self.board_gui.get_figure_by_square_id(square_id)
                    figure.set_dragging(True)
                    figure.set_cord_position_to_center(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_figure_dragging:
                    print("dragging stopped")
                    new_square_id = self.board_gui.get_correlating_square_id_or_none(event.pos)
                    new_square_id = new_square_id if new_square_id is not None else self.id_figure_dragging
                    figure = self.board_gui.get_figure_by_square_id(self.id_figure_dragging)
                    figure.set_dragging(False)
                    print(f"old square id: {self.id_figure_dragging}")
                    print(f"new square id: {new_square_id}")
                    if self.id_figure_dragging != new_square_id:
                        self.board.push(chess.Move.from_uci(f"{figure.chess_position}{chess.square_name(new_square_id)}"))
                        self.board_gui.move_figure(self.id_figure_dragging, new_square_id)
                        self.board_gui.set_figures_according_to_board(self.board)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        self.board_gui.draw_chessboard(surface)
        self.board_gui.draw_figures(surface)

    def update(self, dt):
        pass
