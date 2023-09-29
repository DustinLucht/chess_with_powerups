"""
This module contains the main class ChessWithPowerUps, representing the game.
"""
import sys

import pygame

from settings import Settings
from chess_board import ChessBoard
from gui import GUI
from src.enums import GameState


class ChessWithPowerUps:
    """
    This class represents the game.
    """
    def __init__(self):
        pygame.init()
        self.screen: pygame.display = None
        self.running: bool = True
        self.settings: Settings = Settings()
        self.chess_board: ChessBoard = ChessBoard()
        self.gui: GUI = GUI()
        self.game_state: GameState = GameState.MENU

    def initialize_game(self):
        """
        Initializes the game.
        """
        # Implement the initialization of the game here
        self.screen = pygame.display.set_mode((self.settings.get_screensize_x(), self.settings.get_screensize_y()),
                                              pygame.RESIZABLE)
        pygame.display.set_caption("Schach mit Power-Ups")
        self.gui.initialize(self.screen)

    def run_game(self):
        """
        Runs the game.
        """
        # Implement the game loop here
        while self.running:
            self._handle_events()
            self._handle_state()
            self._draw()

    def _handle_state(self):
        """
        Handles the current state of the game.
        """
        # Implement the state handling here
        pass

    def _handle_events(self):
        """
        Handles the events of the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                print(f"resized to {event.w}x{event.h}")
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.settings.set_screensize(screensize_x=event.w, screensize_y=event.h)
                self.gui.resize()

    def _draw(self):
        """
        Draws the game.
        """
        self.screen.fill((0, 0, 0))
        if self.game_state == GameState.MENU:
            self.gui.draw_menu()
        elif self.game_state == GameState.SETTINGS:
            self.gui.draw_settings()
        elif self.game_state == GameState.PRE_GAME:
            self.gui.draw_pre_game()
        elif self.game_state == GameState.MID_GAME:
            self.gui.draw_game()
        elif self.game_state == GameState.GAME_OVER:
            self.gui.draw_game_over()
        pygame.display.flip()
