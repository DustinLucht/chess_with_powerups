"""
This module contains the classes for the power-ups.
"""
import chess

from ..enums import PowerUpTypes


class PowerUp:
    """
    This class represents a power-up.
    """
    power_up_type: PowerUpTypes

    def __init__(self, power_up_type: PowerUpTypes) -> None:
        self.power_up_type = power_up_type

    def apply_power_up(self, board: chess.Board):
        """
        Applies the power-up.
        :param board: The board on which the power-up is applied
        """
        pass


class DestroyPowerUp(PowerUp):
    def __init__(self):
        super().__init__(PowerUpTypes.DESTROY)

    def apply_power_up(self, board):
        # Implement the logic for the Freeze power-up here
        pass


class DoubleMovePowerUp(PowerUp):
    def __init__(self):
        super().__init__(PowerUpTypes.DOUBLE_MOVE)

    def apply_power_up(self, board):
        # Implement the logic for the DoubleMove power-up here
        pass


class AIHelpsPowerUp(PowerUp):
    def __init__(self):
        super().__init__(PowerUpTypes.AI_HELPS)

    def apply_power_up(self, board):
        # Implement the logic for the AIHelps power-up here
        pass


class RandomPromotionPowerUp(PowerUp):
    def __init__(self):
        super().__init__(PowerUpTypes.RANDOM_PROMOTION)

    def apply_power_up(self, board):
        # Implement the logic for the RandomPromotion power-up here
        pass
