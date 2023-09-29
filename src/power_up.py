"""
This module contains the classes for the power-ups.
"""
from src.enums import PowerUpTypes


class PowerUp:
    """
    This class represents a power-up.
    """
    def __init__(self, power_up_type: PowerUpTypes):
        self.power_up_type: PowerUpTypes = power_up_type

    def apply_power_up(self):
        """
        Applies the power-up.
        """
        pass

class FreezePowerUp(PowerUp):
    def __init__(self):
        super().__init__(PowerUpTypes.FREEZE)

    def apply_power_up(self):
        # Implement the logic for the Freeze power-up here
        pass

class DoubleMovePowerUp(PowerUp):
    def __init__(self):
        super().__init__(PowerUpTypes.DOUBLE_MOVE)

    def apply_power_up(self):
        # Implement the logic for the DoubleMove power-up here
        pass
