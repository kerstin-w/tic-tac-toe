import sys
import time
from colorama import init, Fore
init(autoreset=True)

# Colour library for text stylisation for the game.


class GameColours():
    """
    Contains shortcuts to various colours used in the game.
    """
    G = Fore.GREEN
    R = Fore.RED
    Y = Fore.CYAN

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
