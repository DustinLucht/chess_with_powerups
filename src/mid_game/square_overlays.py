"""
Overlay class.
"""
import pygame

from config.globals import CHESS_BOARD_COLORS
from src.enums import OverlayType, PowerUpTypes
from src.mid_game.power_ups import PowerUp

COLOR_SCHEME = {
    OverlayType.SELECTED_FIGURE: pygame.Color("yellow"),
    OverlayType.POSSIBLE_MOVE_NORMAL: pygame.Color("green"),
    OverlayType.POSSIBLE_MOVE_ATTACK: pygame.Color("red"),
    OverlayType.BACKGROUND: pygame.Color(100, 100, 100),
}


class SquareOverlay:
    """
    Base class for all overlays.
    """
    square_id: int
    overlay_type: OverlayType
    center_pos: tuple[int, int]
    overlay_rect: pygame.Rect
    overlay_surface: pygame.Surface

    def __init__(self, overlay_type: OverlayType, center_pos: tuple[int, int], square_size: int,
                 square_id: int) -> None:
        self.square_id = square_id
        self.overlay_type = overlay_type
        self.center_pos = center_pos
        self.overlay_rect = pygame.Rect(center_pos, (square_size, square_size))
        self.overlay_surface = pygame.Surface((square_size, square_size))

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the overlay.
        :param surface: Surface to draw on
        """
        pass


class SquareOverlayMove(SquareOverlay):
    """
    SquareOverlayMove class.
    """
    overlay_color: pygame.Color

    def __init__(self, overlay_type: OverlayType, center_pos: tuple[int, int], square_size: int, square_id: int):
        super().__init__(overlay_type, center_pos, square_size, square_id)
        x, y = center_pos
        self.overlay_color = COLOR_SCHEME[overlay_type]
        self.overlay_rect = pygame.Rect(x, y, square_size, square_size)
        self.overlay_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        self.overlay_surface.set_alpha(100)

    def draw(self, surface):
        pygame.draw.rect(self.overlay_surface, self.overlay_color, self.overlay_surface.get_rect())
        surface.blit(self.overlay_surface, self.overlay_rect)


class SquareOverlayPromotion(SquareOverlay):
    """
    SquareOverlayPromotion class.
    """
    image_path: str

    def __init__(self, overlay_type: OverlayType, center_pos: tuple[int, int], square_size: int, square_id: int,
                 image_path: str):
        super().__init__(overlay_type, center_pos, square_size, square_id)
        x, y = center_pos
        self.image_path = image_path
        self.overlay_rect = pygame.Rect(x, y, square_size, square_size)
        self._create_overlay_surface_base(square_size)
        self._update_overlay_with_edges()
        self._update_overlay_with_figure(square_size)

    def draw(self, surface):
        surface.blit(self.overlay_surface, self.overlay_rect)

    def _create_overlay_surface_base(self, square_size: int) -> None:
        """
        Creates the base of the overlay surface.
        :param square_size: Size of the square.
        """
        self.overlay_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        # self.overlay_surface.set_alpha(100)
        self.overlay_surface.fill(CHESS_BOARD_COLORS[0])

    def _update_overlay_with_edges(self) -> None:
        """
        Updates the overlay with the edges.
        """
        pygame.draw.rect(self.overlay_surface, pygame.Color("black"), self.overlay_surface.get_rect(), 2)
        pygame.draw.rect(self.overlay_surface, pygame.Color("white"), self.overlay_surface.get_rect().inflate(-2, -2),
                         2)
        pygame.draw.rect(self.overlay_surface, pygame.Color("black"), self.overlay_surface.get_rect().inflate(-4, -4),
                         2)
        pygame.draw.rect(self.overlay_surface, pygame.Color("white"), self.overlay_surface.get_rect().inflate(-6, -6),
                         2)

    def _update_overlay_with_figure(self, square_size: int) -> None:
        """
        Updates the overlay with the figure.
        :param square_size: Size of the square.
        """
        figure = pygame.transform.scale(pygame.image.load(self.image_path), (square_size, square_size))
        self.overlay_surface.blit(figure, (0, 0))


class SquareOverlayPowerUp(SquareOverlay):
    """
    SquareOverlayPowerUp class.
    """
    image_path: str
    powerup: PowerUp

    def __init__(self, overlay_type: OverlayType, center_pos: tuple[int, int], square_size: int, square_id: int,
                 image_path: str, powerup: PowerUp):
        super().__init__(overlay_type, center_pos, square_size, square_id)
        x, y = center_pos
        self.powerup = powerup
        self.image_path = image_path
        self.overlay_rect = pygame.Rect(x, y, square_size, square_size)
        self._create_overlay_surface_base(square_size)
        self._update_overlay_with_figure(square_size)

    def draw(self, surface):
        surface.blit(self.overlay_surface, self.overlay_rect)

    def _create_overlay_surface_base(self, square_size: int) -> None:
        """
        Creates the base of the overlay surface.
        :param square_size: Size of the square.
        """
        self.overlay_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        # self.overlay_surface.set_alpha(100)
        self.overlay_surface.fill(CHESS_BOARD_COLORS[0])

    def _update_overlay_with_figure(self, square_size: int) -> None:
        """
        Updates the overlay with the figure.
        :param square_size: Size of the square.
        """
        figure = pygame.transform.scale(pygame.image.load(self.image_path), (square_size, square_size))
        self.overlay_surface.blit(figure, (0, 0))

    def _update_overlay_with_edges(self) -> None:
        """
        Updates the overlay with the edges.
        """
        pygame.draw.rect(self.overlay_surface, pygame.Color("green"), self.overlay_surface.get_rect(), 2)
        pygame.draw.rect(self.overlay_surface, pygame.Color("green"), self.overlay_surface.get_rect().inflate(-2, -2),
                         2)
        pygame.draw.rect(self.overlay_surface, pygame.Color("green"), self.overlay_surface.get_rect().inflate(-4, -4),
                         2)
        pygame.draw.rect(self.overlay_surface, pygame.Color("green"), self.overlay_surface.get_rect().inflate(-6, -6),
                         2)

    def activate_powerup(self) -> None:
        """
        Gives the powerup to a green edge.
        """
        self.overlay_surface.fill(CHESS_BOARD_COLORS[1])
        self._update_overlay_with_figure(self.overlay_rect.width)
        self._update_overlay_with_edges()


class SquareOverlayPowerupBackground(SquareOverlay):
    """
    SquareOverlayPowerupBackground class.
    """
    overlay_color: pygame.Color

    def __init__(self, overlay_type: OverlayType, center_pos: tuple[int, int], square_size: int, square_id: int):
        super().__init__(overlay_type, center_pos, square_size, square_id)
        x, y = center_pos
        self.overlay_color = COLOR_SCHEME[overlay_type]
        self.overlay_rect = pygame.Rect(x, y, square_size, square_size)
        self.overlay_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)

    def draw(self, surface):
        pygame.draw.rect(self.overlay_surface, self.overlay_color, self.overlay_surface.get_rect())
        surface.blit(self.overlay_surface, self.overlay_rect)