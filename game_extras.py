import sys
import time
from os import system, name
from colorama import init, Fore
init(autoreset=True)

# Colour library for text stylisation for the game.


class GameColours():
    """
    Contains shortcuts to various colours used in the game.
    """
    G = Fore.GREEN
    R = Fore.RED
    M = Fore.MAGENTA
    Y = Fore.CYAN
    RE = Fore.RESET

# Type effect for text in game


def typewriter(string):
    """
    Typewriter for beginning of the game
    The Python code for the typewriter was found here:
    https://replit.com/talk/learn/Typewriter-effect-Python/139897
    """
    for i in string:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.05)

# Validation for user input


def input_with_validation(prompt, valid_options):
    """
    Askes the user to enter en input and checks afterwards,
    if it matches with the valid options.
    If not the user can enter input again.
    """
    while True:
        user_input = input(Fore.CYAN + prompt).lower()
        if user_input not in valid_options:
            print(Fore.MAGENTA + "\nOopsi! Wrong entry.")
            continue
        break
    return user_input


def clear():
    """
    Clear terminal
    """
    # for windows
    if name == "nt":
        _ = system("cls")
    # for mac and linux
    else:
        _ = system("clear")
