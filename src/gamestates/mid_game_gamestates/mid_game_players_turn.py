"""
This module contains the MidGamePlayersTurn class.
"""
import pygame
import chess
from src.enums import ChessColor, MidGamePersistentDataKeys
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState
from src.mid_game.chess_board_gui import ChessBoardGui
from src.mid_game.player import Player


class MidGamePlayersTurn(MidGameBaseState):
    def __init__(self, players_name: str, players_color: ChessColor):
        super(MidGamePlayersTurn, self).__init__()
        # init vars
        self.is_figure_dragging: bool = False
        self.id_figure_dragging: int = 0
        self.player: Player = Player(players_name, players_color)

    def startup(self, mid_game_persistent):
        super(MidGamePlayersTurn, self).startup(mid_game_persistent)
        # init board
        self.board = mid_game_persistent[MidGamePersistentDataKeys.BOARD]
        self.board_gui = mid_game_persistent[MidGamePersistentDataKeys.BOARD_GUI]
        self.board_gui.set_figures_according_to_board(self.board)
        # init background
        self.background_image = mid_game_persistent[MidGamePersistentDataKeys.BACKGROUND_IMAGE]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                square_id = self.board_gui.get_correlating_square_id_or_none(event.pos)
                if square_id is not None:
                    if self.board.piece_at(square_id) is not None:
                        self.is_figure_dragging = True
                        self.id_figure_dragging = square_id
                        figure = self.board_gui.get_figure_by_square_id(square_id)
                        figure.set_dragging(True)
                        figure.set_cord_position_to_center(event.pos)
        if self.is_figure_dragging:
            if event.type == pygame.MOUSEMOTION:
                figure = self.board_gui.get_figure_by_square_id(self.id_figure_dragging)
                figure.set_cord_position_to_center(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    new_square_id = self.board_gui.get_correlating_square_id_or_none(event.pos)
                    new_square_id = new_square_id if new_square_id is not None else self.id_figure_dragging
                    figure = self.board_gui.get_figure_by_square_id(self.id_figure_dragging)
                    figure.set_dragging(False)
                    self.is_figure_dragging = False
                    if self.id_figure_dragging != new_square_id:
                        self.board.push(chess.Move.from_uci(f"{figure.chess_position}{chess.square_name(new_square_id)}"))
                        self.board_gui.move_figure_and_del_old(self.id_figure_dragging, new_square_id)
                    self.board_gui.set_figures_according_to_board(self.board)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        self.board_gui.draw_chessboard(surface)
        self.board_gui.draw_figures(surface)

    def update(self, dt):
        pass
