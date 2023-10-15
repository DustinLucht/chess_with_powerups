"""
This module represents the chess board gui.
"""
import chess
import pygame

from config.globals import CHESS_BOARD_COLORS
from src.enums import OverlayType, ChessColor
from src.mid_game.chess_board_figure import ChessBoardFigure
from src.mid_game.square_overlays import SquareOverlay, SquareOverlayMove, SquareOverlayPromotion

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
    board: chess.Board
    square_size: int
    pieces_size_multiplier: float
    board_rotation: bool
    active_pieces: dict[int, ChessBoardFigure]

    overlays: list[SquareOverlay]
    chess_field_name_to_inde: dict[str, int]
    chess_index_to_field_name: dict[int, str]

    def __init__(self, board: chess.Board, square_size: int, pieces_size_multiplier: float,
                 board_rotation: bool = False):
        # init vars
        self.board = board
        self.square_size = square_size
        self.pieces_size_multiplier = pieces_size_multiplier
        self.board_rotation = board_rotation
        self.active_pieces = {}
        # init figures
        for square_id in board.piece_map():
            figure = board.piece_at(square_id)
            if figure is not None:
                self.active_pieces[square_id] = ChessBoardFigure(square_size * pieces_size_multiplier,
                                                                 f"..\\assets\\images\\pieces\\"
                                                                 f"{PIECES[str(figure)]}",
                                                                 str(figure), chess.square_name(square_id),
                                                                 (0, 0))
        # init overlays
        self.overlays = []
        # init chess field name to index
        self.chess_field_name_to_index = {f"{chr(97 + x)}{y + 1}": x + y * 8 for x in range(8) for y in range(8)}
        self.chess_index_to_field_name = {v: k for k, v in self.chess_field_name_to_index.items()}

    def set_figures_according_to_board(self) -> None:
        """
        Sets the figures.
        """
        current_pieces = self.board.piece_map()

        # Remove pieces that are not on the board anymore or have been replaced
        squares_to_remove = [square for square in self.active_pieces if square not in current_pieces or
                             self.active_pieces[square].name != str(current_pieces[square])]
        for square in squares_to_remove:
            del self.active_pieces[square]

        # Add new pieces or pieces that have been replaced
        for square, piece in current_pieces.items():
            if square not in self.active_pieces:
                self.active_pieces[square] = ChessBoardFigure(self.square_size * self.pieces_size_multiplier,
                                                              f"..\\assets\\images\\pieces\\{PIECES[str(piece)]}",
                                                              str(piece), chess.square_name(square),
                                                              (0, 0))

        # Update the positions of the pieces
        for square, piece in self.active_pieces.items():
            piece.set_chess_position(chess.square_name(square))
            if not piece.is_dragging():
                piece.set_cord_position(
                    self._get_square_coordinates_for_centered_figure(chess.square_name(square), piece.size))

        # Clean all overlays
        self.overlays.clear()

    def set_selected_square(self, square_id: int) -> None:
        """
        Sets the selected square.
        :param square_id: Square id
        """
        # clean all overlays
        self.overlays.clear()

        # add the selected figure overlay
        self.overlays.append(SquareOverlayMove(OverlayType.SELECTED_FIGURE,
                                               self._get_square_coordinates_for_centered_figure(
                                                   chess.square_name(square_id), self.square_size),
                                               self.square_size, square_id))
        # add all possible moves
        for move in self.board.legal_moves:
            if move.from_square == square_id:
                if self.board.piece_at(move.to_square) is None:
                    self.overlays.append(SquareOverlayMove(OverlayType.POSSIBLE_MOVE_NORMAL,
                                                           self._get_square_coordinates_for_centered_figure(
                                                               chess.square_name(move.to_square), self.square_size),
                                                           self.square_size, move.to_square))
                else:
                    self.overlays.append(SquareOverlayMove(OverlayType.POSSIBLE_MOVE_ATTACK,
                                                           self._get_square_coordinates_for_centered_figure(
                                                               chess.square_name(move.to_square), self.square_size),
                                                           self.square_size, move.to_square))

    def set_peasant_promotion_overlay(self, square_id: int, player_color: ChessColor) -> None:
        """
        Sets the selected square.
        :param square_id: Square id
        :param player_color: Player color
        """
        # init
        current_center_pos = self._get_square_coordinates_for_centered_figure(chess.square_name(square_id),
                                                                              self.square_size)
        all_promotion_figures = ["Q", "R", "B", "N"] if player_color == ChessColor.WHITE else ["q", "r", "b", "n"]
        figure_to_promotion_enum = {"Q": OverlayType.PROMOTION_QUEEN, "R": OverlayType.PROMOTION_ROOK,
                                    "B": OverlayType.PROMOTION_BISHOP, "N": OverlayType.PROMOTION_KNIGHT,
                                    "q": OverlayType.PROMOTION_QUEEN, "r": OverlayType.PROMOTION_ROOK,
                                    "b": OverlayType.PROMOTION_BISHOP, "n": OverlayType.PROMOTION_KNIGHT}
        for promotion_figure in all_promotion_figures:
            # add the selected figure overlay
            self.overlays.append(
                SquareOverlayPromotion(figure_to_promotion_enum[promotion_figure], current_center_pos, self.square_size,
                                       square_id, f"..\\assets\\images\\pieces\\{PIECES[promotion_figure]}"))
            current_center_pos = (current_center_pos[0], current_center_pos[1] + self.square_size)

    def set_figure_to_square(self, square_id: int, player_color: ChessColor, selected_promotion: OverlayType) -> None:
        """
        Sets the figure to the square.
        :param square_id: Square id
        :param player_color: Player color
        :param selected_promotion: Selected promotion
        """
        # transform chess color and overlay type to a figure str
        figure_str = "Q" if player_color == ChessColor.WHITE else "q"
        if selected_promotion == OverlayType.PROMOTION_ROOK:
            figure_str = "R" if player_color == ChessColor.WHITE else "r"
        elif selected_promotion == OverlayType.PROMOTION_BISHOP:
            figure_str = "B" if player_color == ChessColor.WHITE else "b"
        elif selected_promotion == OverlayType.PROMOTION_KNIGHT:
            figure_str = "N" if player_color == ChessColor.WHITE else "n"
        # set the figure
        self.active_pieces[square_id] = ChessBoardFigure(self.square_size * self.pieces_size_multiplier,
                                                         f"..\\assets\\images\\pieces\\{PIECES[figure_str]}",
                                                         figure_str, chess.square_name(square_id), (0, 0))

    def get_figure_by_square_id(self, square_id: int) -> ChessBoardFigure:
        """
        Gets the figure by square id.
        :param square_id: Square id
        :return: Figure
        """
        return self.active_pieces[square_id]

    def get_correlating_square_name_or_none(self, pos: tuple) -> str | None:
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

    def get_correlating_square_id_or_none(self, pos: tuple) -> int | None:
        """
        Get the correlating square id or None if not found.
        :param pos: Position of the mouse
        :return: Square id or None
        """
        name = self.get_correlating_square_name_or_none(pos)
        if name not in self.chess_field_name_to_index:
            return None
        return self.chess_field_name_to_index[name]

    def get_selected_promotion(self, mouse_pos: tuple[int, int]) -> OverlayType | None:
        """
        Get the selected promotion.
        :param mouse_pos: Mouse position
        :return: Selected promotion or None
        """
        for overlay in self.overlays:
            if overlay.overlay_type in [OverlayType.PROMOTION_QUEEN, OverlayType.PROMOTION_ROOK,
                                        OverlayType.PROMOTION_BISHOP, OverlayType.PROMOTION_KNIGHT]:
                if overlay.overlay_rect.collidepoint(mouse_pos):
                    return overlay.overlay_type
        return None

    def is_a_overlay_selected(self, square_id: int) -> bool:
        """
        Checks if the overlays are selected.
        :param square_id: Square id
        :return: True if selected, False otherwise
        """
        for overlay in self.overlays:
            if overlay.square_id == square_id:
                return True
        return False

    def is_a_overlay_selected_promotion_dialog(self, mouse_pos: tuple[int, int]) -> bool:
        """
        Checks if the overlays are selected.
        :param mouse_pos: Mouse position
        :return: True if selected, False otherwise
        """
        for overlay in self.overlays:
            if overlay.overlay_rect.collidepoint(mouse_pos):
                return True
        return False

    def is_overlay_selected_figure(self, square_id: int) -> bool:
        """
        Checks if the overlay is selected.
        :param square_id: Square id
        :return: True if selected, False otherwise
        """
        for overlay in self.overlays:
            if overlay.overlay_type == OverlayType.SELECTED_FIGURE and overlay.square_id == square_id:
                return True
        return False

    def rotate_board(self) -> None:
        """
        Rotates the board.
        """
        self.board_rotation = not self.board_rotation

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
        for row in range(8):
            for col in range(8):
                color = CHESS_BOARD_COLORS[(row + col) % 2]

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
