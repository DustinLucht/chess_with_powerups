"""
This module represents the chess board gui.
"""
import chess
import pygame

PIECES_SIZE = 0.7


class ChessBoardGui:
    """
    This class represents the chess board gui.
    """

    def __init__(self, square_size: int, board_rotation: bool = False):
        self.square_size: int = square_size
        self.board_rotation: bool = board_rotation
        self.b_bishop: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\b_bishop_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.b_king: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\b_king_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.b_knight: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\b_knight_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.b_pawn: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\b_pawn_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.b_queen: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\b_queen_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.b_rook: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\b_rook_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.w_bishop: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\w_bishop_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.w_king: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\w_king_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.w_knight: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\w_knight_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.w_pawn: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\w_pawn_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.w_queen: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\w_queen_2x_ns.png"), (square_size * PIECES_SIZE, square_size * PIECES_SIZE))
        self.w_rook: pygame.Surface = pygame.transform.scale(pygame.image.load(
            "..\\assets\\images\\pieces\\w_rook_png_1024px.png"),
            (square_size * PIECES_SIZE, square_size * PIECES_SIZE))

    def get_piece(self, piece) -> pygame.Surface or None:
        """
        Gets the piece.
        :param piece:
        :return: pygame.Surface or None
        """
        if piece == "b":
            return self.b_bishop
        elif piece == "k":
            return self.b_king
        elif piece == "n":
            return self.b_knight
        elif piece == "p":
            return self.b_pawn
        elif piece == "q":
            return self.b_queen
        elif piece == "r":
            return self.b_rook
        elif piece == "B":
            return self.w_bishop
        elif piece == "K":
            return self.w_king
        elif piece == "N":
            return self.w_knight
        elif piece == "P":
            return self.w_pawn
        elif piece == "Q":
            return self.w_queen
        elif piece == "R":
            return self.w_rook
        else:
            return None

    def draw_chessboard(self, surface: pygame.Surface):
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

    def draw_figure(self, surface: pygame.Surface, figure: str, square_id: str):
        """
        Draw a figure on the chessboard.
        :param surface: Surface to draw on
        :param figure: Figure to draw
        :param square_id: Square id
        """
        x1, y1, x2, y2 = self.get_square_coordinates(square_id)
        # center the drawing
        x1 += (self.square_size - self.square_size * PIECES_SIZE) / 2
        y1 += (self.square_size - self.square_size * PIECES_SIZE) / 2
        rect = pygame.Rect(x1, y1, x2, y2)
        surface.blit(self.get_piece(figure), rect)

    def draw_figures(self, surface: pygame.Surface, board: chess.Board):
        """
        Draw all figures on the chessboard.
        :param surface: Surface to draw on
        :param board: Board to draw
        """
        for square_id in chess.SQUARES:
            figure = board.piece_at(square_id)
            if figure is not None:
                self.draw_figure(surface, str(figure), chess.square_name(square_id))

    def get_correlating_square_id_or_none(self, pos: tuple) -> str or None:
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

    def get_square_coordinates(self, square_id: str) -> tuple:
        """
        Get the correlating square coordinates.
        :param square_id: Square id
        :return: Square coordinates
        """
        x, y = square_id
        x = ord(x) - 97
        y = 8 - int(y)

        if self.board_rotation:
            x = 7 - x
            y = 7 - y

        return x * self.square_size, y * self.square_size, x * self.square_size + self.square_size, y * self.square_size + self.square_size
