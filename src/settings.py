"""
Dieses Modul enthält die Klasse Player, die einen Spieler repräsentiert.
"""


class Settings:
    """
    Class for storing settings for the game.
    """

    def __init__(self):
        self.single_player: bool = False
        self.two_players: bool = False
        self.full_screen: bool = False
        self.difficulty: float = 1.0
        self.screensize_x: int = 800
        self.screensize_y: int = 600

    def get_screensize_x(self):
        """
        Returns the x size of the screen.
        :return: screensize_x
        """
        return self.screensize_x

    def get_screensize_y(self):
        """
        Returns the y size of the screen.
        :return: screensize_y
        """
        return self.screensize_y

    def set_screensize(self, screensize_x: int, screensize_y: int):
        """
        Sets the size of the screen.
        :param screensize_x: Die x Größe des Bildschirms
        :param screensize_y: Die y Größe des Bildschirms
        """
        self.screensize_x = screensize_x
        self.screensize_y = screensize_y

    def get_settings_dict(self):
        """
        Returns a dictionary with the settings.
        :return: settings_dict
        """
        return {
            "single_player": self.single_player,
            "two_players": self.two_players,
            "full_screen": self.full_screen,
            "difficulty": self.difficulty,
            "screensize_x": self.screensize_x,
            "screensize_y": self.screensize_y
        }

    def update_settings(self, settings_dict):
        """
        Updates the settings with the given dictionary.
        :param settings_dict: Das Dictionary mit den neuen Einstellungen
        """
        self.single_player = settings_dict["single_player"]
        self.two_players = settings_dict["two_players"]
        self.full_screen = settings_dict["full_screen"]
        self.difficulty = settings_dict["difficulty"]
        self.screensize_x = settings_dict["screensize_x"]
        self.screensize_y = settings_dict["screensize_y"]
