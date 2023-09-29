"""
This module contains the class Settings, which stores game settings.
"""
import json
from pathlib import Path


SETTINGS_PATH = Path(Path.cwd() / "../config/settings.json")


class Settings:
    """
    Class for storing settings for the game.
    """
    def __init__(self):
        self._single_player: bool = False
        self._two_players: bool = False
        self._full_screen: bool = False
        self._difficulty: float = 1.0
        self._screensize_x: int = 800
        self._screensize_y: int = 600
        self._load_settings()

    def get_screensize_x(self):
        """
        Returns the x size of the screen.
        :return: screensize_x
        """
        return self._screensize_x

    def get_screensize_y(self):
        """
        Returns the y size of the screen.
        :return: screensize_y
        """
        return self._screensize_y

    def set_screensize(self, screensize_x: int, screensize_y: int):
        """
        Sets the size of the screen.
        :param screensize_x: The x size of the screen
        :param screensize_y: The y size of the screen
        """
        self._screensize_x = screensize_x
        self._screensize_y = screensize_y

    def get_settings_dict(self):
        """
        Returns a dictionary with the settings.
        :return: settings_dict
        """
        return {
            "single_player": self._single_player,
            "two_players": self._two_players,
            "full_screen": self._full_screen,
            "difficulty": self._difficulty,
            "screensize_x": self._screensize_x,
            "screensize_y": self._screensize_y
        }

    def update_settings(self, settings_dict):
        """
        Updates the settings with the given dictionary.
        :param settings_dict: The dictionary with the new settings
        """
        self._single_player = settings_dict["single_player"]
        self._two_players = settings_dict["two_players"]
        self._full_screen = settings_dict["full_screen"]
        self._difficulty = settings_dict["difficulty"]
        self._screensize_x = settings_dict["screensize_x"]
        self._screensize_y = settings_dict["screensize_y"]

    def _load_settings(self):
        """
        Loads the settings from the settings file.
        """
        # Implement the loading of the settings here
        if SETTINGS_PATH.is_file():
            with open(f"{SETTINGS_PATH}", "r") as f:
                settings_dict = json.load(f)
                self.update_settings(settings_dict)
        else:
            self._save_settings()

    def _save_settings(self):
        """
        Saves the settings to the settings file.
        """
        # Implement the saving of the settings here
        with open(f"{SETTINGS_PATH}", "w") as f:
            json.dump(self.get_settings_dict(), f, indent=4)
