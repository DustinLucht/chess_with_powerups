import pygame

from .base import BaseState
from ..enums import GameState
from pygame_widgets.slider import Slider
from pygame_widgets.toggle import Toggle
from pygame_widgets.button import Button


class PreGame(BaseState):
    def __init__(self):
        super(PreGame, self).__init__()
        self.next_state: GameState = GameState.MID_GAME
        self.font: pygame.font.Font = pygame.font.Font(None, 40)
        self.background_image: pygame.Surface = pygame.Surface(self.screen_rect.size)
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)

        # UI Elemente
        self.textbox_single_player_render: pygame.Surface = self.font.render("Mehrspieler: Aus", True, (255, 255, 255))
        self.toggle_single_player: Toggle = Toggle(pygame.display.get_surface(), 1000, 100, 200, 40,
                                                   fontSize=30, textColour=(255, 255, 255), inactiveColour=(0, 0, 150),
                                                   handleColour=(150, 150, 150), handleRadius=18, initial=True)
        self.textbox_difficulty_render: pygame.Surface = self.font.render("Schwierigkeit: 10.0", True, (255, 255, 255))
        self.slider_difficulty: Slider = Slider(pygame.display.get_surface(), 1000, 250, 800, 40, min=0.1,
                                                max=10, step=0.1, handleColour=(150, 150, 150), handleRadius=18,
                                                initial=1)
        self.textbox_power_up_multiplicator: pygame.Surface = self.font.render("Power Up Muliplicator: 1", True,
                                                                               (255, 255, 255))
        self.slider_power_up_multiplicator: Slider = Slider(pygame.display.get_surface(), 1000, 400, 800, 40, min=1,
                                                            max=10, step=1, handleColour=(150, 150, 150),
                                                            handleRadius=18,
                                                            initial=1)
        self.button_back = Button(pygame.display.get_surface(), 1000, 550, 200, 40, text="Zurück", fontSize=30,
                                  inactiveColour=(141, 185, 244), pressedColour=(50, 50, 255), radius=20,
                                  hoverColour=(100, 100, 255),
                                  onRelease=self.handle_action, onReleaseParams=["Zurück"])
        self.button_start = Button(pygame.display.get_surface(), 1400, 550, 200, 40, text="Start", fontSize=30,
                                   inactiveColour=(141, 185, 244), pressedColour=(50, 50, 255), radius=20,
                                   hoverColour=(100, 100, 255),
                                   onRelease=self.handle_action, onReleaseParams=["Start"])

        self.single_player: bool = True
        self.difficulty: float = 1.0
        self.power_up_multiplicator: int = 1

    def startup(self, persistent):
        super(PreGame, self).startup(persistent)
        self.background_image = persistent["background_image"]
        self.background_rect: pygame.Rect = self.background_image.get_rect(center=self.screen_rect.center)
        self.next_state = GameState.MID_GAME
        self.set_persist()
        self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.background_image, self.background_rect)

        surface.blit(self.textbox_single_player_render, (1000, 50))
        self.toggle_single_player.draw()
        surface.blit(self.textbox_difficulty_render, (1000, 200))
        self.slider_difficulty.draw()
        surface.blit(self.textbox_power_up_multiplicator, (1000, 350))
        self.slider_power_up_multiplicator.draw()
        self.button_back.draw()
        self.button_start.draw()

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def update(self, dt):
        self.textbox_single_player_render = self.get_text_render(
            f"Mehrspieler:  {'An' if self.toggle_single_player.getValue() else 'Aus'}")
        self.textbox_difficulty_render = self.get_text_render(
            f"Schwierigkeit:  {round(self.slider_difficulty.getValue(), 1)}")
        self.textbox_power_up_multiplicator = self.get_text_render(
            f"Power Up Muliplicator:  {round(self.slider_power_up_multiplicator.getValue(), 1)}")

    def get_text_render(self, text: str) -> pygame.Surface:
        """
        Gets the text render.
        :param text:
        :return: Rendered text
        """
        return self.font.render(text, True, (255, 255, 255))

    def handle_action(self, event) -> None:
        """
        Handles the action.
        :param event: Event
        """
        if event == "Zurück":
            self.next_state = GameState.MENU
        elif event == "Start":
            self.next_state = GameState.MID_GAME
            self.set_persist()
        self.done = True

    def set_persist(self) -> None:
        """
        Starts the game.
        """
        self.persist["single_player"] = self.toggle_single_player.getValue()
        self.persist["difficulty"] = self.slider_difficulty.getValue()
        self.persist["power_up_multiplicator"] = self.slider_power_up_multiplicator.getValue()

