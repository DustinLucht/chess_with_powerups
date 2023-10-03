"""
This module contains the MidGamePlayersTurn class.
"""
import pygame
import chess
from src.enums import ChessColor, OverlayType
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState
from src.mid_game.chess_board_figure import ChessBoardFigure
from src.mid_game.chess_board_gui import ChessBoardGui
from src.mid_game.player import Player


class MidGamePlayersTurn(MidGameBaseState):
    def __init__(self, players_name: str, players_color: ChessColor, board: chess.Board, board_gui: ChessBoardGui):
        super(MidGamePlayersTurn, self).__init__()
        # init vars
        self.is_figure_dragging: bool = False
        self.id_square_selected: int = 0
        self.player: Player = Player(players_name, players_color)
        self.time_clicked: float = 0
        self.button_down: bool = False
        self.wait_for_separate_player_input: bool = False
        # init board
        self.board = board
        self.board_gui = board_gui

    def startup(self, mid_game_persistent):
        super(MidGamePlayersTurn, self).startup(mid_game_persistent)
        self.board_gui.set_figures_according_to_board()

    def get_event(self, event):
        if self.wait_for_separate_player_input:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.handle_peasant_promotion(event.pos)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.time_clicked = 0
                    self.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.button_down = False
                    if self.is_figure_dragging:
                        self._handle_releasing_figure(event.pos)
                    if self.time_clicked <= 200:
                        self._handle_short_mousebuttondown(event.pos)

            # only checks when actively dragging a figure
            if self.is_figure_dragging:
                if event.type == pygame.MOUSEMOTION:
                    self._handle_dragging_figure(event.pos)

    def draw(self, surface):
        self.board_gui.draw(surface)

    def update(self, dt):
        self.time_clicked += dt
        if self.time_clicked > 200 and self.button_down:
            self._handle_long_mousebuttondown(pygame.mouse.get_pos())
            self.button_down = False

    def _check_for_peasant_promotion(self, to_square_id: int) -> bool:
        """
        Checks if the peasant is on the last row.
        :param to_square_id: To square id
        :return: True if peasant promotion, False otherwise
        """
        if self.board.piece_at(self.id_square_selected).piece_type == chess.PAWN:
            if self.player.color == ChessColor.WHITE:
                if to_square_id > 55:
                    return True
            else:
                if to_square_id < 8:
                    return True
        return False

    def _handle_long_mousebuttondown(self, mouse_pos: tuple[int, int]) -> None:
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
                    self.id_square_selected = square_id
                    figure = self.board_gui.get_figure_by_square_id(square_id)
                    figure.set_dragging(True)
                    figure.set_cord_position_to_center(mouse_pos)
                    self.board_gui.set_selected_square(square_id)

    def _handle_short_mousebuttondown(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles the mousebuttondown event.
        :param mouse_pos: Position of the mouse
        :return: None
        """
        square_id = self.board_gui.get_correlating_square_id_or_none(mouse_pos)
        # square is not None
        if square_id is not None:
            # check if overlays are selected
            if self.board_gui.is_a_overlay_selected(square_id):
                self._handle_overlay_selected(square_id)
            # check if figure is selected
            elif self.board.piece_at(square_id) is not None:
                if self.board.piece_at(square_id).color == self.player.color.value:
                    self.id_square_selected = square_id
                    self.board_gui.set_selected_square(square_id)

    def _handle_dragging_figure(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles the dragging of a figure.
        :param mouse_pos: Position of the mouse
        :return: None
        """
        figure = self.board_gui.get_figure_by_square_id(self.id_square_selected)
        figure.set_cord_position_to_center(mouse_pos)

    def _handle_releasing_figure(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles the releasing of a figure.
        :param mouse_pos: Position of the mouse
        :return: None
        """
        new_square_id = self.board_gui.get_correlating_square_id_or_none(mouse_pos)
        new_square_id = new_square_id if new_square_id is not None else self.id_square_selected
        figure = self.board_gui.get_figure_by_square_id(self.id_square_selected)
        figure.set_dragging(False)
        self.is_figure_dragging = False
        if self.id_square_selected != new_square_id:
            # check if new square is one of the possible moves
            if self.board_gui.is_a_overlay_selected(new_square_id):
                # check if it is the same color
                if self.board_gui.is_overlay_selected_figure(new_square_id):
                    self.board_gui.set_figures_according_to_board()
                    return
                # else it is an possible move
                self._move_figure(figure, new_square_id)
            else:
                self.board_gui.set_figures_according_to_board()
        else:
            self.board_gui.set_figures_according_to_board()

    def _handle_overlay_selected(self, square_id: int) -> None:
        """
        Handles the selection of an overlay.
        :param square_id: Square id
        :return: None
        """
        figure = self.board_gui.get_figure_by_square_id(self.id_square_selected)
        if self.board_gui.is_overlay_selected_figure(square_id):
            return
        self._move_figure(figure, square_id)

    def _handle_peasant_promotion(self, to_square_id: int) -> None:
        """
        Handles the peasant promotion.
        :param to_square_id: To square id
        :return: None
        """
        self.board_gui.set_peasant_promotion_overlay(to_square_id, self.player.color)
        self.wait_for_separate_player_input = True

    def handle_peasant_promotion(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handles the peasant promotion.
        :param mouse_pos: Position of the mouse
        :return: None
        """
        if self.board_gui.is_a_overlay_selected_promotion_dialog(mouse_pos):
            selected_promotion = self.board_gui.get_selected_promotion(mouse_pos)
            to_square_id = self.id_square_selected + 8 if self.player.color == ChessColor.WHITE else \
                self.id_square_selected - 8
            if not selected_promotion:
                return
            elif selected_promotion == OverlayType.PROMOTION_QUEEN:
                self.board.push(chess.Move.from_uci(
                    f"{self.board_gui.get_figure_by_square_id(self.id_square_selected).chess_position}"
                    f"{chess.square_name(to_square_id)}q"))
            elif selected_promotion == OverlayType.PROMOTION_ROOK:
                self.board.push(chess.Move.from_uci(
                    f"{self.board_gui.get_figure_by_square_id(self.id_square_selected).chess_position}"
                    f"{chess.square_name(to_square_id)}r"))
            elif selected_promotion == OverlayType.PROMOTION_BISHOP:
                self.board.push(chess.Move.from_uci(
                    f"{self.board_gui.get_figure_by_square_id(self.id_square_selected).chess_position}"
                    f"{chess.square_name(to_square_id)}b"))
            elif selected_promotion == OverlayType.PROMOTION_KNIGHT:
                self.board.push(chess.Move.from_uci(
                    f"{self.board_gui.get_figure_by_square_id(self.id_square_selected).chess_position}"
                    f"{chess.square_name(to_square_id)}n"))
            self.wait_for_separate_player_input = False
            self.id_square_selected = -1
            self.board_gui.set_figure_to_square(self.id_square_selected, self.player.color, selected_promotion)
            self.board_gui.set_figures_according_to_board()
            self.done = True

    def _move_figure(self, figure: ChessBoardFigure, to_square_id: int) -> None:
        """
        Moves the figure.
        :param figure: Figure
        :param to_square_id: To square id
        :return: None
        """
        if self._check_for_peasant_promotion(to_square_id):
            self._handle_peasant_promotion(to_square_id)
            return
        self.board.push(chess.Move.from_uci(f"{figure.chess_position}{chess.square_name(to_square_id)}"))
        self.board_gui.move_figure_and_del_old(self.id_square_selected, to_square_id)
        self.board_gui.set_figures_according_to_board()
        self.done = True
