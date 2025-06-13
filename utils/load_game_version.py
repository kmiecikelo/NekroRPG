import configparser
import sys
import os

def resource_path(relative_path):
    """Zwraca poprawną ścieżkę do pliku po spakowaniu przez PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_game_version():
    config = configparser.ConfigParser()
    config_path = resource_path("data/version.ini")
    config.read(config_path)
    return config.get("game", "version", fallback="0.0.0")

CURRENT_GAME_VERSION = get_game_version()
