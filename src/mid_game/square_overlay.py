"""
Overlay class.
"""
import pygame

from src.enums import OverlayType


COLOR_SCHEME = {
    OverlayType.SELECTED_FIGURE: pygame.Color("yellow"),
    OverlayType.POSSIBLE_MOVE_NORMAL: pygame.Color("green"),
    OverlayType.POSSIBLE_MOVE_ATTACK: pygame.Color("red")
}


class SquareOverlay:
    """
    Base class for all overlays.
    """
    def __init__(self, overlay_type: OverlayType, center_pos: tuple[int, int], square_size: int):
        self.overlay_type: OverlayType = overlay_type
        self.overlay_color = COLOR_SCHEME[overlay_type]
        x, y = center_pos
        self.overlay_rect = pygame.Rect(x, y, square_size, square_size)
        self.overlay_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the overlay.
        :param surface: Surface to draw on
        """
        pygame.draw.rect(self.overlay_surface, self.overlay_color, self.overlay_surface.get_rect())
        surface.blit(self.overlay_surface, self.overlay_rect)
