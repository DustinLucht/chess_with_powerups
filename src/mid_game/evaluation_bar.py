import queue
import threading

import chess
import chess.engine
import pygame


COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)


class EvaluationBar:
    """
    This class represents the evaluation bar for the chess engine's evaluation.
    """
    evaluation_value: float
    starting_coordinate: tuple[int, int]
    size: tuple[int, int]
    overlay_rect_white: pygame.Rect
    overlay_surface_white: pygame.Surface
    overlay_rect_black: pygame.Rect
    overlay_surface_black: pygame.Surface
    overlay_rect_full: pygame.Rect
    overlay_surface_full: pygame.Surface

    def __init__(self, starting_coordinate: tuple[int, int], size: tuple[int, int]):
        """
        Initialize the EvaluationBar.
        :param starting_coordinate: The starting position of the bar.
        :param size: The size of the bar.
        """
        # init vars
        self.evaluation_value = 0.0
        self.starting_coordinate = starting_coordinate
        self.size = size
        # init full overlay
        self.overlay_rect_full = pygame.Rect(starting_coordinate[0], starting_coordinate[1], size[0], size[1])
        self.overlay_surface_full = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        self._update_full_overlay_with_edges()
        # init overlays
        self.overlay_rect_white = pygame.Rect(starting_coordinate[0], starting_coordinate[1], size[0], size[1])
        self.overlay_surface_white = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        self.overlay_rect_black = pygame.Rect(starting_coordinate[0], starting_coordinate[1], size[0], size[1])
        self.overlay_surface_black = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        # init overlay rects
        self._update_overlay_rects()

    def _update_full_overlay_with_edges(self) -> None:
        """
        Updates the overlay with the edges.
        """
        pygame.draw.rect(self.overlay_surface_full, pygame.Color("grey"),
                         self.overlay_surface_full.get_rect(), 2)
        pygame.draw.rect(self.overlay_surface_full, pygame.Color("grey"),
                         self.overlay_surface_full.get_rect().inflate(-2, -2), 2)
        pygame.draw.rect(self.overlay_surface_full, pygame.Color("grey"),
                         self.overlay_surface_full.get_rect().inflate(-4, -4), 2)
        pygame.draw.rect(self.overlay_surface_full, pygame.Color("grey"),
                         self.overlay_surface_full.get_rect().inflate(-6, -6), 2)

    def _update_overlay_rects(self) -> None:
        """
        Updates the overlay rects.
        """
        bar_height = self.size[1]  # Gesamthöhe der Balkenanzeige
        white_height = bar_height * (self.evaluation_value + 1) / 2  # Höhe des weißen Balkens
        black_height = bar_height - white_height  # Höhe des schwarzen Balkens

        # Die vertikale Position des schwarzen Balkens bleibt konstant
        self.overlay_rect_black = pygame.Rect(self.starting_coordinate[0], self.starting_coordinate[1],
                                              self.size[0], black_height)

        # Die vertikale Position des weißen Balkens beginnt am Ende des schwarzen Balkens
        self.overlay_rect_white = pygame.Rect(self.starting_coordinate[0], self.starting_coordinate[1] + black_height,
                                              self.size[0], white_height)

    def _update_overlay_surfaces(self) -> None:
        """
        Updates the overlay surfaces.
        """
        self.overlay_surface_white = pygame.Surface((self.overlay_rect_white.width, self.overlay_rect_white.height),
                                                    pygame.SRCALPHA)
        self.overlay_surface_white.fill(COLOR_WHITE)
        self.overlay_surface_black = pygame.Surface((self.overlay_rect_black.width, self.overlay_rect_black.height),
                                                    pygame.SRCALPHA)
        self.overlay_surface_black.fill(COLOR_BLACK)

    def _update_evaluation_threaded(self, board: chess.Board, engine: chess.engine.SimpleEngine, time: float) -> None:
        """
        Update the evaluation value based on the given chess board and engine.
        :param board: The chess board to evaluate.
        :param engine: The chess engine to use for evaluation.
        """
        info = engine.analyse(board, chess.engine.Limit(time=time))
        score = info["score"].white().score() / 100.0  # Convert centipawns to pawns
        # Normalize score between -1 and 1
        normalized_score = max(-1.0, min(1.0, score))
        self._evaluation_callback(normalized_score)

    def _evaluation_callback(self, score: float) -> None:
        """
        Callback after the evaluation is done.
        :param score: The normalized score.
        """
        self.evaluation_value = score
        print("Evaluation: " + str(score))

    def update_evaluation(self, board: chess.Board, engine: chess.engine.SimpleEngine) -> None:
        """
        Update the evaluation value based on the given chess board and engine.
        :param board: The chess board to evaluate.
        :param engine: The chess engine to use for evaluation.
        """
        thread = threading.Thread(target=self._update_evaluation_threaded, args=(board, engine, 0.8))
        thread.start()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the evaluation bar on the given surface.
        """
        # update overlay rects
        self._update_overlay_rects()
        # update overlays
        self._update_overlay_surfaces()
        # overlays
        surface.blit(self.overlay_surface_white, self.overlay_rect_white)
        surface.blit(self.overlay_surface_black, self.overlay_rect_black)
        # full overlay
        surface.blit(self.overlay_surface_full, self.overlay_rect_full)
