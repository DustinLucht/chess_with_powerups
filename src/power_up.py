"""
Dieses Modul enthält die Klassen für die Power-Ups.
"""
from src.enums import PowerUpTypes


class PowerUp:
    """
    Diese Klasse repräsentiert ein Power-Up.
    """
    def __init__(self, power_up_type: PowerUpTypes):
        self.power_up_type: PowerUpTypes = power_up_type

    def apply_power_up(self):
        """
        Wendet das Power-Up an.
        """
        pass


class FreezePowerUp(PowerUp):
    def __init__(self):
        super().__init__(PowerUpTypes.FREEZE)

    def apply_power_up(self):
        # Implementiere die Logik für das Freeze-Power-Up hier
        pass


class DoubleMovePowerUp(PowerUp):
    def __init__(self):
        super().__init__(PowerUpTypes.DOUBLE_MOVE)

    def apply_power_up(self):
        # Implementiere die Logik für das DoubleMove-Power-Up hier
        pass

# Weitere Power-Up-Klassen können nach dem gleichen Muster hinzugefügt werden
