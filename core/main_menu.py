from colorama import init, Fore, Style
from utils.clean_screen import clear
from utils.slow_print import slow_print
init(autoreset=True, convert=True)

def main_menu():
    clear()
    print(Fore.RED + """
    888b    888          888                        8888888b.  8888888b.   .d8888b.
    8888b   888          888                        888   Y88b 888   Y88b d88P  Y88b
    88888b  888          888                        888    888 888    888 888    888
    888Y88b 888  .d88b.  888  888 888d888 .d88b.    888   d88P 888   d88P 888
    888 Y88b888 d8P  Y8b 888 .88P 888P"  d88""88b   8888888P"  8888888P"  888  88888
    888  Y88888 88888888 888888K  888    888  888   888 T88b   888        888    888
    888   Y8888 Y8b.     888 "88b 888    Y88..88P   888  T88b  888        Y88b  d88P
    888    Y888  "Y8888  888  888 888     "Y88P"    888   T88b 888        "Y8888P88  0.0.2
    """)


    print("1. Nowa Gra")
    print("2. Wczytaj Grę")
    print("3. Informacja")
    print("4. Koniec")

    wybor = input(f"\nWpisz komendę: ").lower().strip()

    if wybor in ["1", "nowa", "nowa gra"]:
        return "newgame"
    elif wybor in ["2", "wczytaj", "wczytaj grę"]:
        return "loadgame"
    elif wybor in ["3", "info", "informacja"]:
        clear()
        slow_print("NekroRPG v0.0.2 - by kmiecikelo")
        input("\nNaciśnij Enter aby wrócić...")
        return main_menu()
    elif wybor in ["4", "koniec", "exit"]:
        exit()
    else:
        print("Nieprawidłowa komenda.")
        input("\nNaciśnij Enter aby spróbować ponownie...")
        return main_menu()