"""
This module contains the class GUI, responsible for displaying the chessboard and messages.
"""
import pygame


TEXT_COLOR = (255, 255, 255)


class GUI:
    """
    This class represents the GUI.
    """
    def __init__(self):
        self.current_width: int = 0
        self.current_height: int = 0
        self.font: pygame.font.Font = pygame.font.Font(None, 0)
        self.active_sprites: list[pygame.sprite.Sprite] = []
        self.screen: pygame.surface.Surface = pygame.surface.Surface((0, 0))

    def initialize(self, screen: pygame.display):
        """
        Initializes the GUI.
        """
        self.current_width = screen.get_width()
        self.current_height = screen.get_height()
        self.active_sprites.clear()
        self.font = pygame.font.Font(None, int(self.current_height // 18))
        self.screen: pygame.display = screen

    def draw_menu(self):
        """
        Displays the menu.
        """
        self.active_sprites.clear()
        for i, item in enumerate(["Start Game", "Settings", "Quit"]):
            text = self.font.render(item, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(self.current_width*0.5, self.current_height/3 + i * 50))
            self.screen.blit(text, text_rect)

    def draw_settings(self):
        """
        Displays the settings.
        """
        # Implement the display of the settings here
        pass

    def draw_pre_game(self):
        """
        Displays the pre-game screen.
        """
        # Implement the display of the pre-game screen here
        pass

    def draw_game_over(self):
        """
        Displays the game over screen.
        """
        # Implement the display of the game over screen here
        pass

    def draw_game(self):
        """
        Displays the game.
        """
        # Implement the display of the game here
        pass

    def resize(self):
        """
        Resizes the window.
        """
        # Implement the resizing of the window here
        self.font = pygame.font.Font(None, self.screen.get_height() // 18)

    def _display_board(self):
        """
        Displays the chessboard.
        """
        # Implement the display of the chessboard here
        pass

    def show_message(self, message: str):
        """
        Displays a message.
        :param message: message to be displayed
        """
        # Implement the display of messages here
        pass
