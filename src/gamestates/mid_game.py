"""
MidGame class
"""
import random

import pygame
import chess
import chess.engine

from ..enums import MidGameState, PersistentDataKeys, ChessColor, MidGamePersistentDataKeys, GameState, \
    GlobalConstants, PowerUpTypes
from ..gamestates.base import BaseState
from ..gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState
from ..gamestates.mid_game_gamestates.mid_game_pause import MidGamePause
from ..gamestates.mid_game_gamestates.mid_game_ai_turn import MidGameAiTurn
from ..gamestates.mid_game_gamestates.mid_game_player_turn import MidGamePlayerTurn
from ..mid_game.chess_board_gui import ChessBoardGui
from ..mid_game.player_ui import PlayerUI
from ..mid_game.power_ups import PowerUp, DestroyPowerUp, DoubleMovePowerUp, AIHelpsPowerUp, RandomPromotionPowerUp

SQUARE_SIZE = int(GlobalConstants.Y_SCREEN_SIZE.value * GlobalConstants.SQUARE_SIZE_MULTIPLIER.value)
PIECES_SIZE = GlobalConstants.PIECES_SIZE.value


class MidGame(BaseState):
    """
    This class represents the mid game.
    """
    mid_game_states: dict[MidGameState, MidGameBaseState]
    mid_game_state_name: MidGameState
    mid_game_state: MidGameBaseState
    players_ui: PlayerUI
    board_gui: ChessBoardGui

    def __init__(self):
        super(MidGame, self).__init__()
        # init states
        self.mid_game_states: dict[MidGameState, MidGameBaseState] = {
            MidGameState.PAUSE: MidGamePause(ChessColor.BLACK)}
        self.mid_game_state_name: MidGameState = MidGameState.PAUSE
        self.mid_game_state: MidGameBaseState = self.mid_game_states[self.mid_game_state_name]
        board: chess.Board = chess.Board()
        self.board_gui = ChessBoardGui(board, SQUARE_SIZE, PIECES_SIZE)
        self.players_ui = PlayerUI((SQUARE_SIZE * 8, 0), (GlobalConstants.X_SCREEN_SIZE.value,
                                                          GlobalConstants.Y_SCREEN_SIZE.value))

    def startup(self, persistent):
        super(MidGame, self).startup(persistent)
        # init board
        board: chess.Board = chess.Board()
        self.board_gui = ChessBoardGui(board, SQUARE_SIZE, PIECES_SIZE)
        self.board_gui.set_figures_according_to_board()
        # init background
        self.background_image = persistent[PersistentDataKeys.BACKGROUND_IMAGE]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)
        # init states
        self.mid_game_states = {MidGameState.PAUSE: MidGamePause(ChessColor.BLACK)}
        # single player
        if self.persist[PersistentDataKeys.SINGLE_PLAYER]:
            # start with white
            if self.persist[PersistentDataKeys.STARTS_WITH_WHITE]:
                self.mid_game_states[MidGameState.TURN_PLAYER_1] = MidGamePlayerTurn(ChessColor.WHITE, "Player 1",
                                                                                      board, self.board_gui)
                self.mid_game_states[MidGameState.TURN_PLAYER_2] = MidGameAiTurn(ChessColor.BLACK,
                                                                                 float(self.persist[
                                                                                             PersistentDataKeys.DIFFICULTY]),
                                                                                 board, self.board_gui)
            # start with black
            else:
                self.board_gui.rotate_board()
                self.mid_game_states[MidGameState.TURN_PLAYER_1] = MidGameAiTurn(ChessColor.WHITE,
                                                                                 float(self.persist[
                                                                                             PersistentDataKeys.DIFFICULTY]),
                                                                                 board, self.board_gui)
                self.mid_game_states[MidGameState.TURN_PLAYER_2] = MidGamePlayerTurn(ChessColor.BLACK, "Player 1",
                                                                                      board, self.board_gui)
        # multi player
        else:
            self.mid_game_states[MidGameState.TURN_PLAYER_1] = MidGamePlayerTurn(ChessColor.WHITE, "Player 1", board,
                                                                                  self.board_gui)
            self.mid_game_states[MidGameState.TURN_PLAYER_2] = MidGamePlayerTurn(ChessColor.BLACK, "Player 2", board,
                                                                                  self.board_gui)
        # set first state
        self.mid_game_state_name = MidGameState.TURN_PLAYER_1
        self.mid_game_state = self.mid_game_states[self.mid_game_state_name]
        # set data and start
        mid_game_persist = {
            MidGamePersistentDataKeys.CURRENT_TURN: self.mid_game_state_name,
            MidGamePersistentDataKeys.DRAW_OFFERED: None,
            MidGamePersistentDataKeys.DRAW_ACCEPTED: False,
            MidGamePersistentDataKeys.FORFEIT: False,
            MidGamePersistentDataKeys.RESTART: False
        }
        self.persist[PersistentDataKeys.BOARD_GUI] = self.board_gui
        self.players_ui.change_player(mid_game_persist, self.mid_game_states[self.mid_game_state_name].get_player_or_none())
        self.mid_game_state.startup(mid_game_persist)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                # resume game
                if self.mid_game_state_name == MidGameState.PAUSE:
                    self.mid_game_state.next_state = self.mid_game_state.mid_game_persist[
                        MidGamePersistentDataKeys.CURRENT_TURN]
                    self.flip_state()
                # pause game
                else:
                    self.mid_game_state.next_state = MidGameState.PAUSE
                    self.flip_state()
                    self.mid_game_state.next_state = self.mid_game_state.mid_game_persist[
                        MidGamePersistentDataKeys.CURRENT_TURN]
        self.mid_game_state.get_event(event)
        self.players_ui.get_event(event, self.mid_game_state.activate_powerup)
        # check for draw
        if self.players_ui.mid_game_persist[MidGamePersistentDataKeys.DRAW_ACCEPTED]:
            self._checks_between_moves()

    def update(self, dt):
        if self.mid_game_state.quit:
            # quitting while mid game means that the player ended the game in the pause menu
            self.next_state = GameState.MENU
            self.done = True
        elif self.mid_game_state.done:
            self._checks_between_moves()
            self.flip_state()
        self.mid_game_state.update(dt)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        self.players_ui.draw(surface)
        self.mid_game_state.draw(surface)

    def flip_state(self) -> None:
        """
        Flips the state.
        :return: None
        """
        # check for restart
        if self._get_mid_game_persist(MidGamePersistentDataKeys.RESTART):
            self.next_state = GameState.MID_GAME
            self.done = True
        next_state = self.mid_game_state.next_state
        self.mid_game_state.done = False
        self.mid_game_state_name = next_state
        mid_game_persist = self.mid_game_state.mid_game_persist
        self.mid_game_state = self.mid_game_states[self.mid_game_state_name]
        self.mid_game_state.startup(mid_game_persist)
        # add powerup if player
        if self.mid_game_state.get_player_or_none() is not None:
            self._add_powerup()
        # update ui
        self.players_ui.change_player(mid_game_persist, self.mid_game_state.get_player_or_none())

    def _add_powerup(self) -> None:
        """
        Adds a powerup to the board.
        :return: None
        """
        current_score = self.players_ui.get_current_score()
        player = self.mid_game_state.get_player_or_none()
        if player.color == ChessColor.WHITE:
            if current_score <= -0.1:
                player.add_powerup(self.get_random_powerup_or_none())
        else:
            if current_score >= 0.1:
                player.add_powerup(self.get_random_powerup_or_none())

    def get_random_powerup_or_none(self, power_up_weights=None) -> PowerUp | None:
        """
        Gets a random powerup or None, with individual probabilities for each powerup.
        :param power_up_weights: Dictionary with PowerUpTypes as keys and their weights as values.
        :return: random powerup or None
        """
        multiplier = self.persist[PersistentDataKeys.POWER_UP_MULTIPLICATOR]
        probability = multiplier / 10  # Convert the multiplier into a probability between 0.1 and 1.0

        # Default weights if none provided
        if power_up_weights is None:
            power_up_weights = {
                PowerUpTypes.DESTROY: 0.5,
                PowerUpTypes.DOUBLE_MOVE: 0.5,  # Double move is less likely
                PowerUpTypes.AI_HELPS: 1,
                PowerUpTypes.RANDOM_PROMOTION: 0.8
            }

        # If a random number is less than the probability, we give a power-up
        if random.random() < probability:
            total_weight = sum(power_up_weights.values())
            random_choice = random.uniform(0, total_weight)
            cumulative_weight = 0

            for power_up_type, weight in power_up_weights.items():
                cumulative_weight += weight
                if random_choice <= cumulative_weight:
                    if power_up_type == PowerUpTypes.DESTROY:
                        return DestroyPowerUp()
                    elif power_up_type == PowerUpTypes.DOUBLE_MOVE:
                        return DoubleMovePowerUp()
                    elif power_up_type == PowerUpTypes.AI_HELPS:
                        return AIHelpsPowerUp()
                    elif power_up_type == PowerUpTypes.RANDOM_PROMOTION:
                        return RandomPromotionPowerUp()
                    break

        return None

    def _checks_between_moves(self) -> None:
        """
        Checks if the game is over or if the next player is in check.
        """
        # get ui stuff
        self.mid_game_state.mid_game_persist = self.players_ui.mid_game_persist

        # update ui stuff
        self.players_ui.update_evaluation(self.mid_game_state.board)

        # check if game is over
        outcome = self.mid_game_state.board.outcome()
        if outcome is not None:
            self.persist[PersistentDataKeys.OUTCOME] = outcome
            self.next_state = GameState.POST_GAME
            self.done = True
            return

        # check forfeit
        if self._get_mid_game_persist(MidGamePersistentDataKeys.FORFEIT):
            self.persist[PersistentDataKeys.OUTCOME] = chess.Outcome(chess.Termination.VARIANT_LOSS,
                                                                     self.mid_game_state.color.value)
            self.next_state = GameState.POST_GAME
            self.done = True
            return

        # check old draw offer
        draw_offered = self._get_mid_game_persist(MidGamePersistentDataKeys.DRAW_OFFERED)
        draw_accepted = self._get_mid_game_persist(MidGamePersistentDataKeys.DRAW_ACCEPTED)
        current_player_color = self.mid_game_state.color
        if draw_offered != current_player_color and not draw_accepted:
            self._set_mid_game_persist(MidGamePersistentDataKeys.DRAW_OFFERED, None)
        # normal draw between two players
        elif draw_offered != current_player_color and draw_accepted:
            self.persist[PersistentDataKeys.OUTCOME] = chess.Outcome(chess.Termination.VARIANT_DRAW, None)
            self.next_state = GameState.POST_GAME
            self.done = True
            return
        # draw claimed
        elif not draw_offered and draw_accepted:
            self.persist[PersistentDataKeys.OUTCOME] = chess.Outcome(chess.Termination.VARIANT_DRAW, None)
            self.next_state = GameState.POST_GAME
            self.done = True
            return

        # next state
        if self.mid_game_state_name == MidGameState.TURN_PLAYER_1:
            self.mid_game_state.next_state = MidGameState.TURN_PLAYER_2
        elif self.mid_game_state_name == MidGameState.TURN_PLAYER_2:
            self.mid_game_state.next_state = MidGameState.TURN_PLAYER_1
        # rotate board
        if not self.persist[PersistentDataKeys.SINGLE_PLAYER]:
            self.mid_game_state.board_gui.rotate_board()

    def _set_mid_game_persist(self, key: MidGamePersistentDataKeys, value: object) -> None:
        """
        Sets the mid_game_persist.
        :param key: key
        :param value: value
        :return: None
        """
        self.mid_game_state.mid_game_persist[key] = value

    def _get_mid_game_persist(self, key: MidGamePersistentDataKeys) -> object:
        """
        Gets the mid_game_persist.
        :param key: key
        :return: value
        """
        if key not in self.mid_game_state.mid_game_persist:
            return None
        return self.mid_game_state.mid_game_persist[key]
