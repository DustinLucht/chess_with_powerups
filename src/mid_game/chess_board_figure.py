"""
ChessBoardFigure class
"""
import pygame


class ChessBoardFigure:
    """
    ChessBoardFigure class
    """
    def __init__(self, size: float, image_path: str, name: str, chess_position: str, cord_position: tuple):
        self.name: str = name
        self.size: float = size
        self.chess_position: str = chess_position
        self.cord_position: tuple = cord_position
        self.dragging: bool = False
        self.figure: pygame.Surface = pygame.transform.scale(pygame.image.load(image_path), (size, size))

    def __str__(self):
        return f'Figure {self.name} at {self.chess_position} at {self.cord_position}'

    def __repr__(self):
        return f'Figure {self.figure} at {self.chess_position} at {self.cord_position}'

    def set_chess_position(self, chess_position: str):
        """
        Sets the chess position.
        :param chess_position: Chess position.
        """
        self.chess_position = chess_position

    def set_cord_position(self, cord_position: tuple):
        """
        Sets the cord position.
        :param cord_position: Cord position.
        """
        self.cord_position = cord_position

    def set_cord_position_to_center(self, cord_position: tuple):
        """
        Sets the cord position to center.
        :param cord_position: Cord position.
        """
        self.cord_position = (cord_position[0] - self.size / 2, cord_position[1] - self.size / 2)

    def draw(self, surface: pygame.Surface):
        """
        Draws the figure.
        :param surface:
        """
        surface.blit(self.figure, self.cord_position)

    def is_dragging(self) -> bool:
        """
        Returns if the figure is dragging.
        :return: True if dragging, False otherwise.
        """
        return self.dragging

    def set_dragging(self, dragging: bool) -> None:
        """
        Sets the figure to dragging.
        :param dragging: True if dragging, False otherwise.
        """
        self.dragging = dragging

