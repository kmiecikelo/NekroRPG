import configparser

def get_game_version():
    config = configparser.ConfigParser()
    config.read("data/version.ini")
    return config.get("game", "version", fallback="0.0.0")

CURRENT_GAME_VERSION = get_game_version()