import time

from core.player import Player
from core.main_menu import main_menu
from core.engine import game_loop
from colorama import init, Fore, Style
from scenes.intro import create_player

init(autoreset=True, convert=True)


def main():
    menu = True
    game = False
    createplayer = False

    player = None

    while menu:
        choice = main_menu()
        if choice == "newgame":
            createplayer = True
            menu = False
        elif choice == "loadgame":
            try:
                player = Player.load()
                game = True
                menu = False
            except FileNotFoundError:
                print("Brak zapisu gry!")
                input("\nNaciśnij Enter aby wrócić...")
    if createplayer:
        player = create_player()
        game = True

    while game:
        game_loop(player)


if __name__ == "__main__":
    main()