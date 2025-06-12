from utils.clean_screen import clear
from utils.slow_print import slow_print
from core.player import Player
import time


def create_player():
    # Prolog - wprowadzenie do świata
    clear()
    slow_print("...Ciemność absolutna.")
    time.sleep(1.5)
    clear()
    slow_print("Cisza przerywana jedynie poszumem wiatru niosącego gorący piasek.")
    time.sleep(1.5)
    clear()
    slow_print("Twoje powieki drżą, gdy z wysiłkiem otwierasz oczy. Oślepia Cię palące słońce.")
    time.sleep(1.5)
    clear()
    slow_print("Gardło masz suche jak popiół, a każdy oddech piecze jak ogień.")
    time.sleep(1.5)
    clear()
    slow_print("Wstajesz, oszołomiony. Pamięć to mglista kraina - fragmenty obrazów bez kontekstu.")
    #time.sleep(1.5)
    clear()
    slow_print("W oddali dostrzegasz niewyraźne kontury... może obóz, może ruiny?")
    #time.sleep(1.5)
    clear()
    slow_print("Jedno jest pewne: musisz odnaleźć siebie, zanim odnajdziesz drogę.")
    time.sleep(1.5)
    clear()

    # Wybór imienia
    slow_print("W głowie pojawia się echo... dźwięk, który mógł być Twoim imieniem:")
    time.sleep(1)
    while True:
        name = input("\n> ").strip()
        if name:
            player = Player(name, 50)
            slow_print(f"{name}... brzmi znajomo.")
            break
        clear()
        slow_print("Cisza wypełnia Twój umysł... musisz przypomnieć sobie swoje imię!")


    # Wybór pochodzenia/klasy
    while True:
        clear()
        time.sleep(1)
        slow_print("Zamknij oczy. Co widzisz, gdy sięgasz do najstarszych wspomnień?")
        time.sleep(1.5)
        print("\n1. Ojciec stoi nad Tobą z uniesionym mieczem, krzycząc: 'Twarda stal hartuje charakter!'")
        print("   (Wojownik: +2 do siły)")
        print("2. Zapach zgniłych jabłek na targu, gdy wyrywasz się z uścisku strażnika, śmiejąc się drwiąco")
        print("   (Łotr: +2 do obrony)")
        print("3. Rytualny śpiew dobiegający z drewnianego kręgu, gdzie uczysz się strącać muchy strzałą")
        print("   (Łucznik: +2 do zręczności)")
        choice = input("\nOstatni klarowny obraz to: ").strip()
        clear()
        if choice == "1":
            player.base_strength += 2
            player.klasa = "Wojownik"
            player.update_stats()
            slow_print("Poczucie honoru i stalowy chłód broni w dłoni - to Cię definiuje.")
            break
        elif choice == "2":
            player.base_defence += 2
            player.klasa = "Łotr"
            player.update_stats()
            slow_print("Szeptane plotki i cień w alejach - tam czujesz się jak w domu.")
            break
        elif choice == "3":
            player.base_dexterity += 2
            player.klasa = "Łucznik"
            player.update_stats()
            slow_print("Wiatr we włosach i napięta cięciwa - to Twój naturalny stan.")
            break
        else:
            slow_print("Ból przeszywa skronie... skąd pochodzę?")
            time.sleep(1.5)
            slow_print("Spróbuj jeszcze raz się skupić...")
            clear()

    # Ulepszony wybór rasy
    while True:
        time.sleep(1.5)
        clear()
        slow_print("Patrzysz na swoje dłonie...")
        time.sleep(1)
        slow_print("Skóra opowiada historię Twojego pochodzenia:")
        time.sleep(1.5)
        print("\n1. Szerokie dłonie pokryte bliznami - znak ciężkiej pracy i krótkiego życia")
        print("   (Człowiek: +1 do wszystkich atrybutów)")
        print("2. Smukłe palce o niemal przejrzystej skórze, żyłkach pulsujących magiczną energią")
        print("   (Elf: +3 do zręczności, -1 do siły)")
        print("3. Gruba skóra w odcieniu ziemi, twarda jak kora dębu")
        print("   (Krasnolud: +3 do siły, -1 do zręczności)")
        choice = input("\nTwoja rasa to: ").strip().lower()
        clear()
        if choice in ["1", "człowiek"]:
            player.base_strength += 1
            player.base_dexterity += 1
            player.base_defence += 1
            player.rasa = "Człowiek"
            player.update_stats()
            slow_print("Jesteś dzieckiem przeciętności - ale to właśnie czyni Cię wyjątkowym.")
            slow_print("Twoja adaptowalność to Twój największy atut.")
            break
        elif choice in ["2", "elf"]:
            player.base_dexterity += 3
            player.base_strength -= 1
            player.base_rasa = "Elf"
            player.update_stats()
            slow_print("Sto pokoleń przodków szepcze do Ciebie w języku wiatru.")
            slow_print("Lecz pamiętaj - nieśmiertelność to przekleństwo, nie dar.")
            break
        elif choice in ["3", "krasnolud"]:
            player.base_strength += 3
            player.base_dexterity -= 1
            player.base_rasa = "Krasnolud"
            player.update_stats()
            slow_print("Kamienie śpiewają Ci pieśni gór, a w żyłach płynie magma.")
            slow_print("Twój upór jest legendarny - nawet bogowie się Tobie nie przeciwstawią.")
            break
        else:
            slow_print("W lustrze duszy widzisz tylko zamglone odbicie...")
            time.sleep(1.5)
            clear()

    # Epilog
    time.sleep(1.5)
    clear()
    slow_print(f"{name}... {player.rasa}... {player.klasa}...")
    time.sleep(1.5)
    slow_print("Fragmenty układają się w całość jak puzzle we mgle.")
    time.sleep(1.5)
    slow_print("Nagle słyszysz za sobą chrzęst piasku pod czyimiś stopami...")
    time.sleep(1.5)
    slow_print("'Całe szczęście, że cię znalazłem, zanim zrobiły to hieny' - mówi niski głos.")
    time.sleep(1.5)
    slow_print("'Jutro wyruszamy. Twoja prawdziwa podróż dopiero się zaczyna.'")
    time.sleep(1.5)
    input("\nWciśnij Enter by kontynuować...")
    clear()

    return player