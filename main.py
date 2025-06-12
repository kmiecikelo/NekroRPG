from core.item_manager import ItemManager
from core.player import Player
from core.main_menu import main_menu
from core.engine import game_loop
from colorama import init, Fore, Style
from scenes.intro import create_player
init(autoreset=True)


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
            player = Player.load()
            if player:
                game = True
                menu = False
            else:
                print(Fore.YELLOW + "Wczytywanie nie powiodło się.")
                print("Czy chcesz rozpocząć nową grę? (t/n)")
                while True:
                    wybor = input(Fore.GREEN + "\nWpisz komendę: ").strip().lower()
                    if wybor in ["t", "tak"]:
                        createplayer = True
                        menu = False
                        break
                    elif wybor in ["n", "nie"]:
                        break
                    else:
                        print("Nieprawidłowy wybór.")
    if createplayer:
        player = create_player()
        game = True

    while game:
        game_loop(player)


if __name__ == "__main__":
    main()
    #player = Player.load()
    #game = True
    #menu = False
    #game_loop(player)
