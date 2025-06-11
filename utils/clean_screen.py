import os

def clear():
    # dla Windows
    if os.name == 'nt':
        os.system('cls')
    # dla Linux / macOS
    else:
        os.system('clear')