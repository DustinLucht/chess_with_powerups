"""
This module contains the MidGamePlayersTurn class.
"""
import pygame
import chess
from src.enums import ChessColor, MidGamePersistentDataKeys
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState
from src.mid_game.chess_board_figure import ChessBoardFigure
from src.mid_game.chess_board_gui import ChessBoardGui
from src.mid_game.player import Player


class MidGamePlayersTurn(MidGameBaseState):
    def __init__(self, players_name: str, players_color: ChessColor, board: chess.Board, board_gui: ChessBoardGui):
        super(MidGamePlayersTurn, self).__init__()
        # init vars
        self.is_figure_dragging: bool = False
        self.id_figure_selected: int = 0
        self.player: Player = Player(players_name, players_color)
        self.time_clicked: float = 0
        self.button_down: bool = False
        # init board
        self.board = board
        self.board_gui = board_gui

    def startup(self, mid_game_persistent):
        super(MidGamePlayersTurn, self).startup(mid_game_persistent)
        self.board_gui.set_figures_according_to_board()

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.time_clicked = 0
                self.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.button_down = False
                if self.is_figure_dragging:
                    self.handle_releasing_figure(event.pos)
                if self.time_clicked <= 200:
                    self.handle_short_mousebuttondown(event.pos)

        # only checks when actively dragging a figure
        if self.is_figure_dragging:
            if event.type == pygame.MOUSEMOTION:
                self.handle_dragging_figure(event.pos)

    def draw(self, surface):
        self.board_gui.draw(surface)

    def update(self, dt):
        self.time_clicked += dt
        if self.time_clicked > 200 and self.button_down:
            self.handle_long_mousebuttondown(pygame.mouse.get_pos())
            self.button_down = False

    def handle_long_mousebuttondown(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles the mousebuttondown event.
        :param mouse_pos: Position of the mouse
        :return: None
        """
        square_id = self.board_gui.get_correlating_square_id_or_none(mouse_pos)
        if square_id is not None:
            if self.board.piece_at(square_id) is not None:
                if self.board.piece_at(square_id).color == self.player.color.value:
                    self.is_figure_dragging = True
                    self.id_figure_selected = square_id
                    figure = self.board_gui.get_figure_by_square_id(square_id)
                    figure.set_dragging(True)
                    figure.set_cord_position_to_center(mouse_pos)
                    self.board_gui.set_selected_square(mouse_pos)

    def handle_short_mousebuttondown(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles the mousebuttondown event.
        :param mouse_pos: Position of the mouse
        :return: None
        """
        square_id = self.board_gui.get_correlating_square_id_or_none(mouse_pos)
        if square_id is not None:
            if self.board.piece_at(square_id) is not None:
                if self.board.piece_at(square_id).color == self.player.color.value:
                    self.board_gui.set_selected_square(mouse_pos)

    def handle_dragging_figure(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles the dragging of a figure.
        :param mouse_pos: Position of the mouse
        :return: None
        """
        figure = self.board_gui.get_figure_by_square_id(self.id_figure_selected)
        figure.set_cord_position_to_center(mouse_pos)

    def handle_releasing_figure(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles the releasing of a figure.
        :param mouse_pos: Position of the mouse
        :return: None
        """
        new_square_id = self.board_gui.get_correlating_square_id_or_none(mouse_pos)
        new_square_id = new_square_id if new_square_id is not None else self.id_figure_selected
        figure = self.board_gui.get_figure_by_square_id(self.id_figure_selected)
        figure.set_dragging(False)
        self.is_figure_dragging = False
        if self.id_figure_selected != new_square_id:
            self.move_figure(figure, new_square_id)
        else:
            self.board_gui.set_figures_according_to_board()

    def move_figure(self, figure: ChessBoardFigure, to_square_id: int) -> None:
        """
        Moves the figure.
        :param figure: Figure
        :param to_square_id: To square id
        :return: None
        """
        self.board.push(chess.Move.from_uci(f"{figure.chess_position}{chess.square_name(to_square_id)}"))
        self.board_gui.move_figure_and_del_old(self.id_figure_selected, to_square_id)
        self.board_gui.set_figures_according_to_board()
        self.done = True
