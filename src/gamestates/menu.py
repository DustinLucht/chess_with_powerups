"""
Menu game state
"""
import pygame
from .base import BaseState
from ..enums import GameState


class Menu(BaseState):
    def __init__(self):
        super(Menu, self).__init__()
        self.active_index: int = 0
        self.options: dict[int, str] = {0: "Spiel starten", 1: "Optionen", 2: "Quit Game"}
        self.next_state = GameState.PRE_GAME
        self.font: pygame.font.Font = pygame.font.Font(None, 45)
        self.background_image: pygame.Surface = pygame.Surface(self.screen_rect.size)
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

    def render_text(self, index: int) -> pygame.SurfaceType:
        """
        Renders the text.
        :param index:
        :return:
        """
        color = (141, 185, 244, 255) if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)

    def get_text_position(self, text: pygame.SurfaceType, index: int) -> pygame.Rect:
        """
        Gets the text position.
        :param text:
        :param index:
        :return:
        """
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 100) - 100)
        return text.get_rect(center=center)

    def handle_action(self):
        """
        Handles the action.
        """
        if self.active_index == 0:
            self.next_state = GameState.PRE_GAME
            self.done = True
        if self.active_index == 1:
            self.next_state = GameState.SETTINGS
            # self.done = True
        elif self.active_index == 2:
            self.quit = True

    def decrease_current_index(self) -> None:
        """
        Decreases the current index.
        :return: None
        """
        self.active_index = self.active_index - 1 if self.active_index > 0 else 0

    def increase_current_index(self) -> None:
        """
        Increases the current index.
        :return: None
        """
        self.active_index = self.active_index + 1 if self.active_index < len(self.options) - 1 else len(
            self.options) - 1

    def startup(self, persistent):
        super(Menu, self).startup(persistent)
        self.background_image = persistent["background_image"]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)
        self.next_state = GameState.PRE_GAME
        self.done = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.decrease_current_index()
            elif event.key == pygame.K_DOWN:
                self.increase_current_index()
            elif event.key == pygame.K_RETURN:
                self.handle_action()
            elif event.key == pygame.K_SPACE:
                self.handle_action()
            elif event.key == pygame.K_ESCAPE:
                self.quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_action()
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.active_index = -1
            for index, option in enumerate(self.options):
                text_render = self.render_text(index)
                text_rect = self.get_text_position(text_render, index)
                if text_rect.collidepoint(mouse_pos):
                    self.active_index = index
        elif event.type == pygame.MOUSEWHEEL:
            if event.y < 0:
                self.increase_current_index()
            elif event.y > 0:
                self.decrease_current_index()

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))
