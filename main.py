"""
This is the main file that will be run to start the game.
"""
from src.chess_with_power_ups import ChessWithPowerUps


if __name__ == "__main__":
    game = ChessWithPowerUps()
    game.initialize_game()
    game.handle_state()
