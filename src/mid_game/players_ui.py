"""
This module contains the mid game players ui gamestate.
"""
import chess
import pygame

from src.enums import OverlayType, MidGamePersistentDataKeys
from src.mid_game.player import Player
from src.mid_game.square_overlays import SquareOverlayPowerupBackground


class PlayersUI:
    """
    This class represents the mid game players ui.
    """
    player: Player | None
    mid_game_persist: dict
    starting_coordinate: tuple[int, int]
    size: tuple[int, int]
    background: list[SquareOverlayPowerupBackground]
    draw_offered_in_last_turn: bool

    def __init__(self, starting_coordinate: tuple[int, int], size: tuple[int, int]) -> None:
        # init vars
        self.player = None
        self.mid_game_persist = {}
        self.starting_coordinate = starting_coordinate
        self.size = size
        self.draw_offered_in_last_turn = True
        # init background
        square_size = int((size[0] - (starting_coordinate[0] + 100)) * 0.25)
        self.background = []
        for i in range(1, 5):
            self.background.append(SquareOverlayPowerupBackground(
                OverlayType.BACKGROUND,
                (size[0] - i * (square_size + 5), self.starting_coordinate[1] + 5),
                square_size, 0))
        # offer
        x_size_of_remaining_space = (size[0] - starting_coordinate[0])
        self.offer_rect = pygame.Rect(starting_coordinate[0] + x_size_of_remaining_space * 0.5 - 150, size[1] * 0.5, 300, 100)
        label = f"Draw anbieten"
        font = pygame.font.Font(None, 36)
        self.offer_text = font.render(label, True, (0, 0, 0))
        self.offer_text_rect = self.offer_text.get_rect(center=self.offer_rect.center)
        # draw accept offer
        self.accept_rect = pygame.Rect(starting_coordinate[0] + x_size_of_remaining_space * 0.5 - 150, size[1] * 0.5 + 200, 300, 100)
        label = f"Draw akzeptieren"
        self.accept_text = font.render(label, True, (0, 0, 0))
        self.accept_text_rect = self.accept_text.get_rect(center=self.accept_rect.center)

    def change_player(self, mid_game_persistent: dict, player: Player) -> None:
        """
        Changes to the player.
        :param player: player
        :param mid_game_persistent: mid_game_persistent data
        """
        self.mid_game_persist = mid_game_persistent
        self.player = player
        self.draw_offered_in_last_turn = True

    def get_event(self, event: pygame.event.Event, board: chess.Board) -> None:
        """
        Gets an event.
        :param board: board
        :param event: event
        """
        if self.player is not None:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for i in range(4):
                        if self.background[i].overlay_rect.collidepoint(event.pos):
                            self.player.use_powerup(i, board)
                    if self.offer_rect.collidepoint(event.pos):
                        if self.mid_game_persist[MidGamePersistentDataKeys.DRAW_OFFERED] is None:
                            self.mid_game_persist[MidGamePersistentDataKeys.DRAW_OFFERED] = self.player.color
                            self.draw_offered_in_last_turn = False
                    if self.accept_rect.collidepoint(event.pos):
                        self.mid_game_persist[MidGamePersistentDataKeys.DRAW_ACCEPTED] = True

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the state.
        :param surface: surface
        """
        for background in self.background:
            background.draw(surface)
        # offer
        self._draw_offer(surface)

    def _draw_offer(self, surface: pygame.Surface) -> None:
        """
        Draws the offer.
        :param surface: surface
        :return: None
        """
        # offer
        color = (100, 100, 100)
        if self.player is not None:
            if self.mid_game_persist[MidGamePersistentDataKeys.DRAW_OFFERED] is None:
                color = (220, 220, 220)
        pygame.draw.rect(surface, color, self.offer_rect)
        surface.blit(self.offer_text, self.offer_text_rect)
        # draw accept offer
        color = (100, 100, 100)
        if self.player is not None:
            if self.mid_game_persist[MidGamePersistentDataKeys.DRAW_OFFERED] is not None:
                if self.draw_offered_in_last_turn:
                    color = (220, 220, 220)
        pygame.draw.rect(surface, color, self.accept_rect)
        surface.blit(self.accept_text, self.accept_text_rect)
