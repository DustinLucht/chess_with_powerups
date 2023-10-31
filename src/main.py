"""
This is the main file that will be run to start the game.
"""
import sys

import pygame

from src.enums import GameState, GlobalConstants
from src.game import Game
from src.gamestates.menu import Menu
from src.gamestates.mid_game import MidGame
from src.gamestates.post_game import PostGame
from src.gamestates.pre_game import PreGame
from src.gamestates.settings import Settings
from src.gamestates.splash import Splash


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((GlobalConstants.X_SCREEN_SIZE.value, GlobalConstants.Y_SCREEN_SIZE.value))
    pygame.display.set_caption("Schach mit Power-Ups")
    states = {
        GameState.SPLASH: Splash(),
        GameState.MENU: Menu(),
        GameState.SETTINGS: Settings(),
        GameState.PRE_GAME: PreGame(),
        GameState.MID_GAME: MidGame(),
        GameState.POST_GAME: PostGame(),
    }

    game = Game(screen, states, GameState.SPLASH)
    game.run()

    pygame.quit()
    sys.exit()
