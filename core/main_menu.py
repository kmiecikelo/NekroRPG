import time

from colorama import init, Fore, Style
from utils.clean_screen import clear
from utils.slow_print import slow_print
from utils.load_game_version import CURRENT_GAME_VERSION

init(autoreset=True)  # ważne, żeby kolory resetowały się automatycznie

def main_menu():
    clear()
    slow_print(f"""
    ooooo      ooo oooooooooooo oooo    oooo ooooooooo.     .oooooo.   <blue> ooooooooo.   ooooooooo.     .oooooo.  </blue>  
    `888b.     `8' `888'     `8 `888   .8P'  `888   `Y88.  d8P'  `Y8b  <blue>`888   `Y88. `888   `Y88.  d8P'  `Y8b  </blue> 
     8 `88b.    8   888          888  d8'     888   .d88' 888      888 <blue> 888   .d88'  888   .d88' 888          </blue> 
     8   `88b.  8   888oooo8     88888[       888ooo88P'  888      888 <blue> 888ooo88P'   888ooo88P'  888          </blue> 
     8     `88b.8   888    "     888`88b.     888`88b.    888      888 <blue> 888`88b.     888         888     ooooo</blue> 
     8       `888   888       o  888  `88b.   888  `88b.  `88b    d88' <blue> 888  `88b.   888         `88.    .88' </blue> 
    o8o        `8  o888ooooood8 o888o  o888o o888o  o888o  `Y8bood8P'  <blue>o888o  o888o o888o         `Y8bood8P'  </blue> 
    Wersja: {CURRENT_GAME_VERSION}
    """ , Fore.RED, delay=0.00)
    time.sleep(0.5)
    slow_print("=" * 50, Fore.CYAN, delay=0.01)
    slow_print("  1. Nowa Gra", Fore.YELLOW, random_delay=True)
    slow_print("  2. Wczytaj Grę", random_delay=True)
    slow_print("  3. Informacja", random_delay=True)
    slow_print("  4. Koniec", Fore.YELLOW, random_delay=True)
    slow_print("=" * 50, Fore.CYAN, delay=0.01)

    wybor = input(Fore.GREEN + "\nWpisz komendę: " + Style.RESET_ALL).lower().strip()

    if wybor in ["1", "nowa", "nowa gra"]:
        return "newgame"

    elif wybor in ["2", "wczytaj", "wczytaj grę"]:
        return "loadgame"

    elif wybor in ["3", "info", "informacja"]:
        clear()
        slow_print("NekroRPG v0.0.2 - by <blue>kmiecikelo</blue>", Fore.YELLOW, random_delay=True)
        input(Fore.GREEN + "\nNaciśnij Enter aby wrócić..." + Style.RESET_ALL)
        return main_menu()

    elif wybor in ["4", "koniec", "exit"]:
        print(Fore.RED + "\nDo zobaczenia!" + Style.RESET_ALL)
        exit()

    else:
        print(Fore.RED + "Nieprawidłowa komenda." + Style.RESET_ALL)
        input(Fore.GREEN + "\nNaciśnij Enter aby spróbować ponownie..." + Style.RESET_ALL)
        return main_menu()