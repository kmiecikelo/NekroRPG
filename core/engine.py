import random
import time
import textwrap
from colorama import init, Fore, Style

from core.item_manager import ItemManager
from utils.clean_screen import clear


def game_loop(player):
    clear()
    while True:
        loc = player.lm.get_location(player.location)
        npcs = player.lm.get_npcs(player.location)
        items = loc.get("items")
        if loc:
            print("\n" + Fore.CYAN + "=" * 20 + " LOKACJA " + "=" * 20)
            print(f"{Fore.YELLOW}Nazwa: {Style.BRIGHT}{loc['name']}")
            print(f"{Fore.YELLOW}Opis: {Style.RESET_ALL}{textwrap.fill(loc['description'], width=70)}\n")
            if items:
                print(f"{Fore.YELLOW}Przedmioty w lokacji:")
                for item_id, qty in items.items():
                    item = player.item_manager.get_item(item_id)
                    if item:
                        if qty > 1:
                            print(f" - {Fore.GREEN}{item['name']} (x{qty}) {Style.RESET_ALL} {item['description']}")
                        else:
                            print(f" - {Fore.GREEN}{item['name']} {Style.RESET_ALL} {item['description']}")
                    else:
                        print(f"  - {item_id} (nieznany przedmiot)")
                print()

            exits = loc.get("exits", {})
            exits_desc = []
            for direction, dest_id in exits.items():
                dest_loc = player.lm.get_location(dest_id)
                dest_name = dest_loc['name'] if dest_loc else "Nieznana lokacja"
                exits_desc.append(f"{Fore.GREEN}{direction}{Style.RESET_ALL} ({dest_name})")

            print(f"{Fore.YELLOW}Dostępne wyjścia: " + ", ".join(exits_desc))
        else:
            print(Fore.RED + "\nNieznana lokacja.")

        if npcs:
            print(f"\n{Fore.YELLOW}Spotykasz NPC:")
            for npc in npcs:
                print(f"- {Fore.GREEN}{npc['name']} - {Style.RESET_ALL}{textwrap.fill(npc['description'], width=70)}")
        else:
            print("Nie ma tu nikogo...")

        print("\n" + Fore.CYAN + "=" * 23 + " MENU " + "=" * 23)
        print("stat / statystyki / info – pokaż status gracza")
        print("inv / eq / ekwipunek / inventory – pokaż ekwipunek gracza")
        print("zapisz / save - zapisz stan gry")
        print("north / south / east / west – porusz się w danym kierunku")
        print("exit / koniec  – wyjdź z gry")

        wybor = input(
            f"\n{Fore.RED}{Style.BRIGHT}<hp{player.hp}/{player.max_hp}>{Style.RESET_ALL} "
            f"{Fore.YELLOW}{Style.BRIGHT}<g{player.gold}>{Style.RESET_ALL} "
            f"{Fore.BLUE}{Style.BRIGHT}<exp{player.exp}/{player.exp_to_next_level()}>{Style.RESET_ALL} "
            f"{Fore.CYAN}{Style.BRIGHT}>>{Style.RESET_ALL} "
        ).lower().strip()

        if wybor in ["stat", "statystyki", "info", "informacje", "stats"]:
            player.status()
        elif wybor in ["inv", "eq", "ekwipunek", "inventory"]:
            player.show_inventory()
        elif wybor in ["exit", "koniec"]:
            exit()
        elif wybor == "exp100":
            player.gain_exp(100)
        elif wybor == "exp1000":
            player.gain_exp(1000)
        elif wybor == "addsword":
            player.add_item("sword_01", 1)
        elif wybor in ["zapisz", "save"]:
            player.save()
            print(Fore.GREEN + "Gra zapisana!")
            time.sleep(0.8)
            clear()
        elif wybor in ["north", "south", "east", "west", "up", "down"]:
            player.move(wybor)
            time.sleep(0.5)
            clear()
        elif wybor.startswith("pick ") or wybor.startswith("weź "):
            parts = wybor.split()
            if len(parts) < 2:
                print(Fore.RED + "Podaj nazwę przedmiotu do podniesienia.")
                time.sleep(1)
                clear()
                continue
            # nazwa przedmiotu może mieć spacje, ostatni element może być liczbą (ilością)
            if parts[-1].isdigit():
                amount = int(parts[-1])
                item_name = " ".join(parts[1:-1]).lower()
            else:
                amount = 1
                item_name = " ".join(parts[1:]).lower()
            # Znajdź ID przedmiotu po nazwie w lokalnych przedmiotach
            found_item_id = None
            loc_items = loc.get("items", {})
            for item_id in loc_items:
                item = player.item_manager.get_item(item_id)
                if item and item['name'].lower() == item_name:
                    found_item_id = item_id
                    break
            if not found_item_id:
                print(Fore.RED + f"Nie ma takiego przedmiotu '{item_name}' w lokacji.")
            else:
                available = loc_items[found_item_id]
                if amount > available:
                    print(Fore.RED + f"Nie ma tyle przedmiotów do podniesienia (dostępne: {available}).")
                else:
                    player.pickitem(found_item_id, amount)
            clear()
        else:
            print(Fore.RED + random.choice([
                "Nie rozumiem.",
                "Hmmm??",
                "Co to ma znaczyć?",
                "Spróbuj jeszcze raz.",
                "Nie mam pojęcia o co chodzi.",
                "Co?"
            ]))
            time.sleep(0.8)
            clear()