from core.item_manager import ItemManager
from core.player import Player
from core.main_menu import main_menu
from core.engine import game_loop
from colorama import init, Fore, Style
from scenes.intro import create_player
init(autoreset=True)


def main():
    item_manager = ItemManager()
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
                player.item_manager = item_manager
                game = True
                menu = False
            except FileNotFoundError:
                print("Brak zapisu gry!")
                print("Chcesz zacząć nową grę? (t/n)")
                wybor = input(Fore.GREEN + "\nWpisz komendę: " + Style.RESET_ALL).lower().strip()

                if wybor in ["t", "tak", "yes"]:
                    createplayer = True
                    menu = False
                elif wybor in ["n", "nie", "no"]:
                    continue
    if createplayer:
        player = create_player()
        player.item_manager = item_manager
        game = True

    while game:
        game_loop(player)


if __name__ == "__main__":
    #main()
    item_manager = ItemManager()
    player = Player.load()
    player.item_manager = item_manager
    game = True
    menu = False
    game_loop(player)