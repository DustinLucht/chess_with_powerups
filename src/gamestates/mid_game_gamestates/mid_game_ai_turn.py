"""
Game Over State
"""
import chess
import chess.engine
import threading

from ...config.globals import ENGINE_PATH
from ...enums import ChessColor
from ...gamestates.mid_game_gamestates.mid_game_base import MidGameBaseState
from ...mid_game.chess_board_gui import ChessBoardGui


class MidGameAiTurn(MidGameBaseState):
    """
    This class represents the post game.
    """
    ais_strength: float
    engine: chess.engine.SimpleEngine

    def __init__(self, color: ChessColor, ais_strength: float, board: chess.Board, board_gui: ChessBoardGui) -> None:
        super(MidGameAiTurn, self).__init__(color)
        # init vars
        self.ais_strength = ais_strength
        self.board = board
        self.board_gui = board_gui
        # Load Stockfish engine
        self.engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

    def startup(self, mid_game_persistent):
        super(MidGameAiTurn, self).startup(mid_game_persistent)
        # Make the AI move in a separate process
        self._make_ai_move()

    def draw(self, surface):
        self.board_gui.draw(surface)

    def _ai_play(self, board, time_limit, queue):
        result = self.engine.play(board, chess.engine.Limit(time=time_limit))
        queue.put(result)

    def _callback(self, result):
        self.board.push(result.move)
        self._i_am_done()

    def _make_ai_move(self):
        """
        Makes the AI move in a separate thread.
        """
        # Set the AI's thinking time based on the difficulty
        time_limit = self.ais_strength  # You can adjust this based on your requirements

        thread = threading.Thread(target=self._ai_play_threaded, args=(self.board, time_limit))
        thread.start()

    def _ai_play_threaded(self, board, time_limit):
        result = self.engine.play(board, chess.engine.Limit(time=time_limit))
        self._callback(result)

    def _i_am_done(self):
        """
        Called when the AI is done with its move.
        :return:
        """
        self.board_gui.set_figures_according_to_board()
        self.done = True
