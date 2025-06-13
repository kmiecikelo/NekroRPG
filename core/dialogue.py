from colorama import Fore, Style
from utils.clean_screen import clear
import textwrap


class DialogueOption:
    def __init__(self, text, response, next_node=None, reward=None, condition=None):
        self.text = text
        self.response = response
        self.next_node = next_node
        self.reward = reward
        self.condition = condition


class DialogueNode:
    def __init__(self, text, options=None):
        self.text = text
        self.options = options or []


class NPC:
    def __init__(self, name, description, dialogues):
        self.name = name
        self.description = description
        self.dialogues = self._parse_dialogues(dialogues)
        self.current_dialogue = "start"

    def _parse_dialogues(self, dialogues_data):
        """Konwertuje dialogi ze słownika na obiekty DialogueNode"""
        dialogues = {}
        for key, node_data in dialogues_data.items():
            options = []
            for option_data in node_data.get("options", []):
                option = DialogueOption(
                    text=option_data["text"],
                    response=option_data["response"],
                    next_node=option_data.get("next_node"),
                    reward=option_data.get("reward"),
                    condition=option_data.get("condition")
                )
                options.append(option)
            dialogues[key] = DialogueNode(node_data["text"], options)
        return dialogues

    def start_dialogue(self, player):
        """Rozpoczyna dialog z graczem"""
        print("\n" + Fore.CYAN + "=" * 20 + " DIALOG " + "=" * 20)
        print(f"{Fore.YELLOW}{self.name}: {Style.RESET_ALL}{self.dialogues[self.current_dialogue].text}\n")

        available_options = []
        for option in self.dialogues[self.current_dialogue].options:
            if option.condition is None or self._check_condition(player, option.condition):
                available_options.append(option)

        # Jeśli nie ma dostępnych opcji, pokaż tylko odpowiedź i zakończ dialog
        if not available_options:
            print(f"{Fore.RED}Brak dostępnych opcji dialogowych.")
            input(Fore.GREEN + "\nNaciśnij Enter aby kontynuować..." + Style.RESET_ALL)
            return None

        # Wyświetl dostępne opcje
        for i, option in enumerate(available_options, 1):
            print(f"{Fore.GREEN}{i}. {Style.RESET_ALL}{option.text}")

        print(f"\n{Fore.RED}0. {Style.RESET_ALL}Wyjdź z rozmowy")
        return available_options

    def _check_condition(self, player, condition):
        """Sprawdza warunek dialogu"""
        if condition is None:
            return True
        elif isinstance(condition, str):
            try:
                return eval(condition, {}, {"p": player})
            except:
                return False
        return False

    def process_choice(self, choice_index, available_options, player):
        """Przetwarza wybór gracza"""
        if choice_index == 0:
            return False  # Wyjście z dialogu

        if choice_index > len(available_options):
            return True  # Kontynuuj dialog, ale pokaż błąd

        selected_option = available_options[choice_index - 1]

        # Wyświetl odpowiedź NPC
        print(f"\n{Fore.YELLOW}{self.name}: {Style.RESET_ALL}{selected_option.response}")

        # Przyznaj nagrodę jeśli istnieje
        if selected_option.reward:
            self._give_reward(selected_option.reward, player)

        # Przejdź do następnego węzła jeśli istnieje
        if selected_option.next_node:
            self.current_dialogue = selected_option.next_node

        # Zawsze kontynuuj dialog, chyba że wybrano opcję wyjścia (0)
        return True

    def _give_reward(self, reward, player):
        """Przyznaje nagrodę graczowi"""
        if isinstance(reward, str):
            # Przedmiot
            player.add_item(reward, 1)
            item = player.item_manager.get_item(reward)
            print(f"\n{Fore.GREEN}Otrzymałeś: {item['name']}!")
        elif isinstance(reward, dict):
            # Statystyki lub złoto
            if 'gold' in reward:
                player.gold += reward['gold']
                print(f"\n{Fore.YELLOW}Otrzymałeś {reward['gold']} złota!")
            if 'stats' in reward:
                player.add_stats(**reward['stats'])

        input(Fore.GREEN + "\nNaciśnij Enter aby kontynuować..." + Style.RESET_ALL)