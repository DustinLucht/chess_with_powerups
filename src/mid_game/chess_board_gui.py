"""
This module represents the chess board gui.
"""
import chess
import pygame

from src.enums import OverlayType
from src.mid_game.chess_board_figure import ChessBoardFigure
from src.mid_game.square_overlay import SquareOverlay

PIECES = {
    "b": "b_bishop_png_1024px.png",
    "k": "b_king_png_1024px.png",
    "n": "b_knight_png_1024px.png",
    "p": "b_pawn_png_1024px.png",
    "q": "b_queen_png_1024px.png",
    "r": "b_rook_png_1024px.png",
    "B": "w_bishop_png_1024px.png",
    "K": "w_king_png_1024px.png",
    "N": "w_knight_png_1024px.png",
    "P": "w_pawn_png_1024px.png",
    "Q": "w_queen_2x_ns.png",
    "R": "w_rook_png_1024px.png"
}


class ChessBoardGui:
    """
    This class represents the chess board gui.
    """

    def __init__(self, board: chess.Board, square_size: int, pieces_size_multiplier: float,
                 board_rotation: bool = False):
        self.board: chess.Board = board
        self.square_size: int = square_size
        self.pieces_size_multiplier: float = pieces_size_multiplier
        self.board_rotation: bool = board_rotation
        self.active_pieces: dict[int, ChessBoardFigure] = {}
        for square_id in board.piece_map():
            figure = board.piece_at(square_id)
            if figure is not None:
                self.active_pieces[square_id] = ChessBoardFigure(square_size * pieces_size_multiplier,
                                                                 f"..\\assets\\images\\pieces\\"
                                                                 f"{PIECES[str(figure)]}",
                                                                 str(figure), chess.square_name(square_id),
                                                                 (0, 0))
        self.overlays: list[SquareOverlay] = []
        self.chess_field_name_to_index = {f"{chr(97 + x)}{y + 1}": x + y * 8 for x in range(8) for y in range(8)}
        self.chess_index_to_field_name = {v: k for k, v in self.chess_field_name_to_index.items()}

    def set_figures_according_to_board(self) -> None:
        """
        Sets the figures.
        :param board: Board
        """
        for square_id in self.board.piece_map():
            figure = self.board.piece_at(square_id)
            if figure is not None:
                piece = self.active_pieces.get(square_id)
                piece.set_chess_position(chess.square_name(square_id))
                if not piece.is_dragging():
                    piece.set_cord_position(
                        (self._get_square_coordinates_for_centered_figure(chess.square_name(square_id), piece.size)))
        # find all pieces that are not on the board anymore
        pieces_to_remove = []
        for square_id in self.active_pieces:
            if square_id not in self.board.piece_map():
                pieces_to_remove.append(square_id)
        # remove them
        for square_id in pieces_to_remove:
            del self.active_pieces[square_id]

    def set_selected_square(self, mouse_pos: tuple[int, int]) -> None:
        """
        Sets the selected square.
        :param mouse_pos: Position of the mouse
        """
        self.overlays.clear()
        square_id = self.get_correlating_square_id_or_none(mouse_pos)
        if square_id is not None:
            self.overlays.append(SquareOverlay(OverlayType.SELECTED_FIGURE,
                                               self._get_square_coordinates_for_centered_figure(
                                                   chess.square_name(square_id), self.square_size),
                                               self.square_size))
            for move in self.board.legal_moves:
                if move.from_square == square_id:
                    if self.board.piece_at(move.to_square) is None:
                        self.overlays.append(SquareOverlay(OverlayType.POSSIBLE_MOVE_NORMAL,
                                                           self._get_square_coordinates_for_centered_figure(
                                                               chess.square_name(move.to_square), self.square_size),
                                                           self.square_size))
                    else:
                        self.overlays.append(SquareOverlay(OverlayType.POSSIBLE_MOVE_ATTACK,
                                                           self._get_square_coordinates_for_centered_figure(
                                                               chess.square_name(move.to_square), self.square_size),
                                                           self.square_size))

    def get_figure_by_square_id(self, square_id: int) -> ChessBoardFigure:
        """
        Gets the figure by square id.
        :param square_id: Square id
        :return: Figure
        """
        return self.active_pieces[square_id]

    def get_correlating_square_name_or_none(self, pos: tuple) -> str or None:
        """
        Get the correlating square id or None if not found.
        :param pos: Position of the mouse
        :return: Square id or None
        """
        x, y = pos
        if self.board_rotation:
            x = 960 - x
            y = 960 - y

        if x < 0 or y < 0:
            return None

        if x > 960 or y > 960:
            return None

        x = x // self.square_size
        y = y // self.square_size

        return f"{chr(97 + x)}{8 - y}"

    def get_correlating_square_id_or_none(self, pos: tuple) -> str or None:
        """
        Get the correlating square id or None if not found.
        :param pos: Position of the mouse
        :return: Square id or None
        """
        name = self.get_correlating_square_name_or_none(pos)
        if name not in self.chess_field_name_to_index:
            return None
        return self.chess_field_name_to_index[name]

    def move_figure_and_del_old(self, old_square_id: int, new_square_id: int) -> None:
        """
        Moves the figure.
        :param old_square_id: Old square id
        :param new_square_id: New square id
        """
        self.overlays.clear()
        self.active_pieces[new_square_id] = self.active_pieces[old_square_id]
        del self.active_pieces[old_square_id]

    def rotate_board(self) -> None:
        """
        Rotates the board.
        """
        self.board_rotation = not self.board_rotation
        self.overlays.clear()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the chessboard.
        :param surface: Surface to draw on
        """
        self._draw_chessboard(surface)
        self._draw_figures(surface)
        self._draw_overlays(surface)

    def _draw_chessboard(self, surface: pygame.Surface) -> None:
        """
        Creates a chessboard.
        :param surface: Surface to draw on
        """
        colors = [(255, 206, 158), (209, 139, 71)]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]

                if self.board_rotation:
                    rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size,
                                       self.square_size)
                    label = f"{chr(104 - col)}{row + 1}"
                else:
                    rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size,
                                       self.square_size)
                    label = f"{chr(97 + col)}{8 - row}"

                pygame.draw.rect(surface, color, rect)

                font = pygame.font.Font(None, 36)
                text = font.render(label, True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                surface.blit(text, text_rect)

    def _draw_figures(self, surface: pygame.Surface) -> None:
        """
        Draw all figures on the chessboard.
        :param surface: Surface to draw on
        """
        drag_piece, drag_rect = None, None
        for name, piece in self.active_pieces.items():
            x1, y1 = piece.cord_position
            rect = pygame.Rect(x1, y1, x1, y1)
            if piece.is_dragging():
                drag_piece = piece
                drag_rect = rect
            else:
                surface.blit(piece.figure, rect)
        if drag_piece is not None:
            surface.blit(drag_piece.figure, drag_rect)

    def _draw_overlays(self, surface: pygame.Surface) -> None:
        """
        Draw all overlays on the chessboard.
        :param surface: Surface to draw on
        """
        for overlay in self.overlays:
            overlay.draw(surface)

    def _get_square_coordinates(self, square_name: str) -> tuple:
        """
        Get the correlating square coordinates.
        :param square_name: square_name
        :return: Square coordinates
        """
        x, y = square_name
        x = ord(x) - 97
        y = 8 - int(y)

        if self.board_rotation:
            x = 7 - x
            y = 7 - y

        return (x * self.square_size, y * self.square_size, x * self.square_size + self.square_size,
                y * self.square_size + self.square_size)

    def _get_square_coordinates_for_centered_figure(self, square_name: str, figure_size: float) -> tuple[int, int]:
        """
        Get the center square coordinates.
        :param square_name: square_name
        :return: Square coordinates
        """
        x1, y1, x2, y2 = self._get_square_coordinates(square_name)
        return (x1 + (self.square_size - figure_size) / 2,
                y1 + (self.square_size - figure_size) / 2)
