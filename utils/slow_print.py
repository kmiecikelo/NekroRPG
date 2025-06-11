import time
import random
import colorama
from colorama import Fore, Back, Style

colorama.init()


def hide_cursor():
    """Ukrywa kursor w terminalu"""
    print("\033[?25l", end="", flush=True)


def show_cursor():
    """Pokazuje kursor w terminalu"""
    print("\033[?25h", end="", flush=True)


def slow_print(text, base_color=Fore.WHITE, delay=0.05, hide_cursor_flag=True,
               end='\n', random_delay=False, min_delay=0.01, max_delay=0.05):
    """
    Powolne drukowanie tekstu z możliwością zmiany kolorów w trakcie

    Parameters:
        text (str): Tekst z znacznikami kolorów np. "<red>czerwony tekst</red>"
        base_color: Domyślny kolor tekstu
        delay (float): Podstawowe opóźnienie między znakami
        hide_cursor_flag (bool): Czy ukryć kursor
        end (str): Znak końca linii
        random_delay (bool): Czy używać losowego opóźnienia
        min_delay/max_delay (float): Zakres losowego opóźnienia
    """
    if hide_cursor_flag:
        hide_cursor()

    try:
        current_color = base_color
        i = 0
        n = len(text)

        while i < n:
            if text[i] == '<' and i + 1 < n:
                # Znaleziono potencjalny znacznik koloru
                end_tag_pos = text.find('>', i)
                if end_tag_pos != -1:
                    tag = text[i + 1:end_tag_pos]

                    # Obsługa znaczników kolorów
                    if tag.startswith('/'):
                        # Zamknięcie znacznika - wróć do base_color
                        current_color = base_color
                        i = end_tag_pos + 1
                        continue
                    elif tag in ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'white']:
                        # Ustaw nowy kolor
                        color_map = {
                            'red': Fore.RED,
                            'blue': Fore.BLUE,
                            'green': Fore.GREEN,
                            'yellow': Fore.YELLOW,
                            'cyan': Fore.CYAN,
                            'magenta': Fore.MAGENTA,
                            'white': Fore.WHITE
                        }
                        current_color = color_map[tag]
                        i = end_tag_pos + 1
                        continue

            # Drukuj znak z aktualnym kolorem
            print(current_color + text[i], end='', flush=True)

            # Oblicz opóźnienie
            current_delay = delay
            if random_delay:
                current_delay = random.uniform(min_delay, max_delay)
            time.sleep(current_delay)

            i += 1

        print(Style.RESET_ALL, end=end)
    finally:
        if hide_cursor_flag:
            show_cursor()


# Przykłady użycia
#    slow_print("<red>To jest czerwony tekst</red>, a to jest <blue>niebieski tekst</blue>")
#    slow_print("Normalny tekst, <green>zielony fragment</green>, znów normalny")
#    slow_print("<red>Czerwony</red>-<blue>Niebieski</blue>-<green>Zielony</green>-<yellow>Żółty</yellow>", delay=0.03)