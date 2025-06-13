import random
import time
import textwrap
from colorama import init, Fore, Style
from utils.clean_screen import clear


def game_loop(player):
    clear()
    while True:
        loc = player.lm.get_location(player.location)
        npcs = player.lm.get_npcs(player.location)

        print("\n" + Fore.CYAN + "=" * 20 + " LOKACJA " + "=" * 20)
        print(f"{Fore.YELLOW}Nazwa: {Style.BRIGHT}{loc['name']}")
        print(f"{Fore.YELLOW}Opis: {Style.RESET_ALL}{textwrap.fill(loc['description'], width=70)}\n")

        if 'items' in loc and loc['items']:
            print(f"{Fore.YELLOW}Przedmioty w lokacji:")
            for item_id, qty in loc['items'].items():
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
        if exits:
            print(f"\n{Fore.YELLOW}Dostępne wyjścia:")
            for direction, dest_id in exits.items():
                dest = player.lm.get_location(dest_id)
                print(f"- {Fore.GREEN}{direction}{Style.RESET_ALL} → {dest['name']}")

        if npcs:
            print(f"\n{Fore.YELLOW}Spotykasz:")
            for npc in npcs:
                print(f"- {Fore.GREEN}{npc['name']}{Style.RESET_ALL}: {textwrap.fill(npc['description'], width=70)}")
        else:
            print("Nie ma tu nikogo...")

        print("\n" + Fore.CYAN + "=" * 23 + " MENU " + "=" * 23)
        print("stat / info / statystyki - status gracza")
        print("inv / plecak  - plecak")
        print("eq / wyposażenie / wypos - zarządzanie ekwipunkiem")
        print("n/s/e/w/u/d - ruch")
        print("weź <nazwa> [ilość] - podnieś przedmiot")
        print("użyj <nazwa> - użyj przedmiotu")
        print("załóż <nazwa> / eq <nazwa> - załóż przedmiot")
        print("zdejmij <slot> / unequip <slot> - zdejmij przedmiot")
        print("zapisz - zapisz grę")
        print("wyjście, exit, quit - zakończ grę")
        print("help - pomoc")

        wybor = input(
            f"\n{Fore.RED}❤️ {player.hp}/{player.max_hp} | "
            f"{Fore.YELLOW}💰 {player.gold} | "
            f"{Fore.BLUE}⚔️ {player.strength} | "
            f"{Fore.GREEN}🛡️ {player.defence} | "
            f"{Fore.MAGENTA}🏹 {player.dexterity} | "
            f"{Fore.MAGENTA}📈 {player.exp}/{player.exp_to_next_level()}\n"
            f"{Fore.CYAN}>> {Style.RESET_ALL}"
        ).lower().strip()

        if wybor in ["stat", "statystyki", "info", "informacje", "stats"]:
            player.status()
        elif wybor in ["inv", "plecak", "inventory"]:
            player.show_inventory()
        elif wybor in ["wyposażenie", "equip", "wypos", "eq"]:
            player.show_equipment()
        elif wybor.startswith(("rozmawiaj ", "talk ", "mów ", "rozmowa ")):
            npc_name = wybor.split(maxsplit=1)[1]
            player.talk_to_npc(npc_name)
            clear()
        elif wybor in ["wyjście", "exit", "quit"]:
            if input("Na pewno chcesz wyjść? (t/n): ").lower() == 't':
                exit()
        elif wybor == "exp100":
            player.gain_exp(100)
        elif wybor == "exp1000":
            player.gain_exp(1000)
        elif wybor == "addsword":
            player.add_item("iron_sword", 1)
        elif wybor == "dajsile":
            player.add_stats(strength=5)
        elif wybor.startswith(("załóż ", "equip ", "eq ", "zaloz ")):
            item_name = wybor.split(maxsplit=1)[1]
            found_item = None
            for item_id in player.inventory:
                item = player.item_manager.get_item(item_id)
                if item and item['name'].lower() == item_name.lower():
                    found_item = item_id
                    break

            if not found_item:
                print(Fore.RED + f"Nie masz przedmiotu: {item_name}")
                time.sleep(1)
            else:
                player.equip(found_item)
            clear()
        elif wybor.startswith(("zdejmij ", "unequip ", "ue ")):
            slot = wybor.split(maxsplit=1)[1]
            if slot in player.equipment:
                player.unequip(slot)
            else:
                print(Fore.RED + f"Nieprawidłowy slot: {slot}")
                time.sleep(1)
            clear()
        elif wybor in ["zapisz", "save"]:
            player.save()
            print(Fore.GREEN + "Gra została zapisana!")
            time.sleep(1)
            clear()
        elif wybor in ["north", "n", "south", "s", "east", "e", "west", "w", "up", "down", "u", "d"]:
            direction = {
                "n": "north",
                "s": "south",
                "e": "east",
                "w": "west",
                "u": "up",
                "d": "down"
            }.get(wybor, wybor)
            player.move(direction)
            time.sleep(0.5)
            clear()
        elif wybor.startswith("pick ") or wybor.startswith("weź "):
            parts = wybor.split()
            if len(parts) < 2:
                print(Fore.RED + "Podaj nazwę przedmiotu do podniesienia.")
                time.sleep(1)
                clear()
                continue

            if parts[-1].isdigit():
                amount = int(parts[-1])
                item_name = " ".join(parts[1:-1]).lower()
            else:
                amount = 1
                item_name = " ".join(parts[1:]).lower()

            found_item_id = None
            loc_items = loc.get("items", {})

            for item_id in loc_items:
                item = player.item_manager.get_item(item_id)
                if item and item['name'].lower() == item_name:
                    found_item_id = item_id
                    break

            if not found_item_id:
                print(Fore.RED + f"Nie ma takiego przedmiotu '{item_name}' w lokacji.")
                time.sleep(1)
            else:
                available = loc_items[found_item_id]
                if amount > available:
                    print(Fore.RED + f"Nie ma tyle przedmiotów do podniesienia (dostępne: {available}).")
                    time.sleep(1)
                else:
                    player.pickitem(found_item_id, amount)
            clear()
        elif wybor.startswith("użyj ") or wybor.startswith("use "):
            item_name = wybor.split(maxsplit=1)[1]
            # Tutaj dodaj implementację użycia przedmiotu
            print(Fore.YELLOW + "Funkcjonalność użycia przedmiotu nie jest jeszcze zaimplementowana.")
            time.sleep(1)
            clear()
        elif wybor == "help":
            # Tutaj możesz dodać bardziej szczegółową pomoc
            print(Fore.YELLOW + "Lista dostępnych komend jest wyświetlona w menu.")
            time.sleep(1)
            clear()
        else:
            print(Fore.RED + random.choice([
                "Nie rozumiem. Wpisz 'help' aby zobaczyć listę komend",
                "Hmmm?? Wpisz 'help' aby zobaczyć listę komend",
                "Co to ma znaczyć? Wpisz 'help' aby zobaczyć listę komend"
            ]))
            time.sleep(0.8)
            clear()