from colorama import init, Fore, Style
import time
init(autoreset=True, convert=True)

def slow_print(text, delay=0.08):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()