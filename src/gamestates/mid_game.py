"""
MidGame class
"""
import pygame
import chess

from src.enums import MidGameState, PersistentDataKeys, ChessColor, MidGamePersistentDataKeys, GameState
from src.gamestates.base import BaseState
from src.gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState
from src.gamestates.mid_game_gamestates.mid_game_pause import MidGamePause
from src.gamestates.mid_game_gamestates.mid_game_ais_turn import MidGameAIsTurn
from src.gamestates.mid_game_gamestates.mid_game_players_turn import MidGamePlayersTurn
from src.mid_game.chess_board_gui import ChessBoardGui

SQUARE_SIZE = 120
PIECES_SIZE = 0.7


class MidGame(BaseState):
    def __init__(self):
        super(MidGame, self).__init__()
        # init states
        self.mid_game_states: dict[MidGameState, MidGameBaseState] = {MidGameState.PAUSE: MidGamePause()}
        self.mid_game_state_name: MidGameState = MidGameState.PAUSE
        self.mid_game_state: MidGameBaseState = self.mid_game_states[self.mid_game_state_name]
        # background
        self.background_image: pygame.Surface = pygame.Surface(self.screen_rect.size)
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

    def startup(self, persistent):
        super(MidGame, self).startup(persistent)
        # init board
        board: chess.Board = chess.Board()
        board_gui: ChessBoardGui = ChessBoardGui(board, SQUARE_SIZE, PIECES_SIZE)
        board_gui.set_figures_according_to_board()
        # init background
        self.background_image = persistent[PersistentDataKeys.BACKGROUND_IMAGE]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)
        # init states
        self.mid_game_states = {MidGameState.PAUSE: MidGamePause()}
        # single player
        if self.persist[PersistentDataKeys.SINGLE_PLAYER]:
            # start with white
            if self.persist[PersistentDataKeys.STARTS_WITH_WHITE]:
                self.mid_game_states[MidGameState.PLAYERS_1_TURN] = MidGamePlayersTurn("Player 1", ChessColor.WHITE,
                                                                                       board, board_gui)
                self.mid_game_states[MidGameState.PLAYERS_2_TURN] = MidGameAIsTurn(
                    float(self.persist[PersistentDataKeys.DIFFICULTY]), ChessColor.BLACK, board, board_gui)
            # start with black
            else:
                board_gui.rotate_board()
                self.mid_game_states[MidGameState.PLAYERS_1_TURN] = MidGameAIsTurn(
                    float(self.persist[PersistentDataKeys.DIFFICULTY]), ChessColor.WHITE, board, board_gui)
                self.mid_game_states[MidGameState.PLAYERS_2_TURN] = MidGamePlayersTurn("Player 1", ChessColor.BLACK,
                                                                                       board, board_gui)
        # multi player
        else:
            self.mid_game_states[MidGameState.PLAYERS_1_TURN] = MidGamePlayersTurn("Player 1", ChessColor.WHITE, board,
                                                                                   board_gui)
            self.mid_game_states[MidGameState.PLAYERS_2_TURN] = MidGamePlayersTurn("Player 2", ChessColor.BLACK, board,
                                                                                   board_gui)
        # set first state
        self.mid_game_state_name = MidGameState.PLAYERS_1_TURN
        self.mid_game_state = self.mid_game_states[self.mid_game_state_name]
        # set data and start
        mid_game_persist = {
            MidGamePersistentDataKeys.CURRENT_TURN: self.mid_game_state_name
        }
        self.mid_game_state.startup(mid_game_persist)

    def flip_state(self) -> None:
        """
        Flips the state.
        :return: None
        """
        next_state = self.mid_game_state.next_state
        self.mid_game_state.done = False
        self.mid_game_state_name = next_state
        mid_game_persist = self.mid_game_state.mid_game_persist
        self.mid_game_state = self.mid_game_states[self.mid_game_state_name]
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
        self.mid_game_state.get_event(event)

    def update(self, dt):
        if self.mid_game_state.quit:
            self.done = True
        elif self.mid_game_state.done:
            self.checks_between_moves()
            self.flip_state()
        self.mid_game_state.update(dt)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        self.mid_game_state.draw(surface)

    def checks_between_moves(self):
        """
        Checks if the game is over or if the next player is in check.
        """
        # next state
        if self.mid_game_state_name == MidGameState.PLAYERS_1_TURN:
            self.mid_game_state.next_state = MidGameState.PLAYERS_2_TURN
        elif self.mid_game_state_name == MidGameState.PLAYERS_2_TURN:
            self.mid_game_state.next_state = MidGameState.PLAYERS_1_TURN
        # rotate board
        if not self.persist[PersistentDataKeys.SINGLE_PLAYER]:
            self.mid_game_state.board_gui.rotate_board()
        # check if game is over
        if self.mid_game_state.board.is_game_over():
            self.next_state = GameState.POST_GAME
            self.done = True

