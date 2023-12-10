"""
This module contains the mid game players ui gamestate.
"""
import chess.engine
import pygame

from src.enums import OverlayType, MidGamePersistentDataKeys, PowerUpTypes
from src.mid_game.evaluation_bar import EvaluationBar
from src.mid_game.player import Player
from src.mid_game.square_overlays import SquareOverlayPowerupBackground, SquareOverlayPowerUp

POWERUPS_IMAGE_PATHS = {
    PowerUpTypes.DESTROY: r"..\assets\images\powerups\craiyon_184052_chess_pawn_logo_on_fire_with_dark_background.png",
    PowerUpTypes.DOUBLE_MOVE: r"..\assets\images\powerups\craiyon_184729_black_chess_pawn_with_a__2x__marking.png",
    PowerUpTypes.AI_HELPS: r"..\assets\images\powerups\craiyon_184158_A_Robot_staring_at_a_chess_board.png",
    PowerUpTypes.RANDOM_PROMOTION: r"..\assets\images\powerups\craiyon_184538_A_chess_pawn_with_a_large_question_mark_"
                                   r"above_it__surrounded_by_silhouettes_of_higher.png",
}


class PlayerUI:
    """
    This class represents the mid game players ui.
    """
    player: Player | None
    mid_game_persist: dict
    starting_coordinate: tuple[int, int]
    size: tuple[int, int]
    background: list[SquareOverlayPowerupBackground]
    powerups: list[SquareOverlayPowerUp]
    powerup_is_active: bool
    draw_offered_in_last_turn: bool
    evaluation_bar: EvaluationBar

    def __init__(self, starting_coordinate: tuple[int, int], size: tuple[int, int]) -> None:
        # init vars
        self.player = None
        self.mid_game_persist = {}
        self.starting_coordinate = starting_coordinate
        self.size = size
        self.draw_offered_in_last_turn = True
        self.powerup_is_active = False
        # init background
        square_size = int((size[0] - (starting_coordinate[0] + 100)) * 0.25)
        self.background = []
        for i in range(1, 5):
            self.background.append(SquareOverlayPowerupBackground(
                OverlayType.BACKGROUND,
                (size[0] - i * (square_size + 5), self.starting_coordinate[1] + 5),
                square_size, 0))
        self.powerups = []
        # offer
        x_size_of_remaining_space = (size[0] - starting_coordinate[0])
        self.offer_rect = pygame.Rect(starting_coordinate[0] + x_size_of_remaining_space * 0.5 - 150, size[1] * 0.5,
                                      300, 100)
        label = f"Draw anbieten"
        font = pygame.font.Font(None, 36)
        self.offer_text = font.render(label, True, (0, 0, 0))
        self.offer_text_rect = self.offer_text.get_rect(center=self.offer_rect.center)
        # accept offer
        self.accept_rect = pygame.Rect(starting_coordinate[0] + x_size_of_remaining_space * 0.5 - 150,
                                       size[1] * 0.5 + 200, 300, 100)
        label = f"Draw akzeptieren"
        self.accept_text = font.render(label, True, (0, 0, 0))
        self.accept_text_rect = self.accept_text.get_rect(center=self.accept_rect.center)
        # evaluation bar
        bar_starting_coordinate = (self.starting_coordinate[0] + 15, 10)
        bar_size = (50, size[1] - 20)
        self.evaluation_bar = EvaluationBar(bar_starting_coordinate, bar_size)

    def change_player(self, mid_game_persistent: dict, player: Player | None) -> None:
        """
        Changes to the player.
        :param player: player
        :param mid_game_persistent: mid_game_persistent data
        """
        self.mid_game_persist = mid_game_persistent
        self.player = player
        self.draw_offered_in_last_turn = True
        self.powerup_is_active = False
        # init powerups
        self.powerups = []
        square_size = int((self.size[0] - (self.starting_coordinate[0] + 100)) * 0.25)
        if player is not None:
            for i, powerup in enumerate(player.get_powerups()):
                self.powerups.append(SquareOverlayPowerUp(
                    OverlayType.POWERUP,
                    (self.size[0] - (i + 1) * (square_size + 5), self.starting_coordinate[1] + 5),
                    square_size, 0, POWERUPS_IMAGE_PATHS[powerup.power_up_type], powerup))

    def get_event(self, event: pygame.event.Event, activate_powerup_function: callable) -> None:
        """
        Gets an event.
        :param activate_powerup_function: activate powerup function
        :param event: event
        """
        if self.player is not None:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if not self.powerup_is_active:
                        for powerup_overlay in self.powerups:
                            if powerup_overlay.overlay_rect.collidepoint(event.pos):
                                activate_powerup_function(powerup_overlay.powerup)
                                self.player.use_powerup(powerup_overlay.powerup)
                                powerup_overlay.activate_powerup()
                                self.powerup_is_active = True
                                break
                    if self.offer_rect.collidepoint(event.pos):
                        if self.mid_game_persist[MidGamePersistentDataKeys.DRAW_OFFERED] is None:
                            self.mid_game_persist[MidGamePersistentDataKeys.DRAW_OFFERED] = self.player.color
                            self.draw_offered_in_last_turn = False
                    if self.accept_rect.collidepoint(event.pos):
                        if self.mid_game_persist[MidGamePersistentDataKeys.DRAW_OFFERED] is not None:
                            self.mid_game_persist[MidGamePersistentDataKeys.DRAW_ACCEPTED] = True

    def get_current_score(self) -> float:
        """
        Gets the current score.
        :return: current score
        """
        return self.evaluation_bar.evaluation_value

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the state.
        :param surface: surface
        """
        # background
        for background in self.background:
            background.draw(surface)
        # powerups
        for powerup in self.powerups:
            powerup.draw(surface)
        # offer
        self._draw_offer(surface)
        self.evaluation_bar.draw(surface)

    def update_evaluation(self, board: chess.Board) -> None:
        """
        Updates the evaluation.
        :param board: chess board
        :return:
        """
        self.evaluation_bar.update_evaluation(board)

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
