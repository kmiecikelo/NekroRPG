import os
from colorama import init, Fore, Style
init(autoreset=True, convert=True)

def clear():
    # dla Windows
    if os.name == 'nt':
        os.system('cls')
    # dla Linux / macOS
    else:
        os.system('clear')