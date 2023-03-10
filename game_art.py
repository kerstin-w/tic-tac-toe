"""
ASCII art to illustrate the game better
"""
from game_extras import GameColours as C


# Logo for the start of the game
LOGO = (
    C.M
    + r"""
-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-

     ______  ____   __      ______   ____    __      ______   ___     ___
    |      ||    | /  ]    |      | /    |  /  ]    |      | /   \   /  _]
    |      | |  | /  /     |      ||  o  | /  /     |      ||     | /  [_
    |_|  |_| |  |/  /      |_|  |_||     |/  /      |_|  |_||  O  ||    _]
      |  |   |  /   \_       |  |  |  _  /   \_       |  |  |     ||   [_
      |  |   |  \     |      |  |  |  |  \     |      |  |  |     ||     |
      |__|  |____\____|      |__|  |__|__|\____|      |__|   \___/ |_____|


-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-
"""
)

# Rules of the game
GAME_RULES = (
    C.Y
    + r"""
    _________________________________________________________________________
   |   ___________________________________________________________________   |
   |  |                                                                   |  |
   |  |                ===============================                    |  |
   |  |                | |                         | |                    |  |
   |  |                | |   G A M E   R U L E S   | |                    |  |
   |  |                | |                         | |                    |  |
   |  |                ===============================                    |  |
   |  |                                                                   |  |
   |  |  1 - The two players take turns placing their symbol(i.e.,        |  |
   |  |      crosses and circles) in the empty boxes on the board.        |  |
   |  |  2 - The goal is to place your own symbol three times in a row,   |  |
   |  |      in a column or in a diagonal.                                |  |
   |  |  3 - The first player to succeed wins the round.                  |  |
   |  |  4 - We are going to play 5 rounds and at the end the winner      |  |
   |  |      is determined.                                               |  |
   |  |___________________________________________________________________|  |
   |_________________________________________________________________________|


-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

"""
)

# Score after each round
SCORE = (
    C.Y
    + r"""
===============================================================================
    C U R R E N T  S C O R E:
"""
)

# Logo for the next round in the game
NEXT_ROUND = (
    C.M
    + r"""
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
        _   __             __     ____                            __ __
       / | / /___   _  __ / /_   / __ \ ____   __  __ ____   ____/ // /
      /  |/ // _ \ | |/_// __/  / /_/ // __ \ / / / // __ \ / __  // /
     / /|  //  __/_>  < / /_   / _, _// /_/ // /_/ // / / // /_/ //_/
    /_/ |_/ \___//_/|_| \__/  /_/ |_| \____/ \__,_//_/ /_/ \__,_/(_)

-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

"""
)

# Leaderboard to show after game is finished
LEADERBOARD = (
    C.Y
    + r"""
=============================================================
                    L E A D E R B O A R D
=============================================================
POS             NAME                 SCORE           DATE
=============================================================
"""
)

# Game over logo
GAME_OVER = (
    C.M
    + r"""
-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
       ______                           ____                        __
      / ____/____ _ ____ ___   ___     / __ \ _   __ ___   _____   / /
     / / __ / __ `// __ `__ \ / _ \   / / / /| | / // _ \ / ___/  / /
    / /_/ // /_/ // / / / / //  __/  / /_/ / | |/ //  __// /     /_/
    \____/ \__,_//_/ /_/ /_/ \___/   \____/  |___/ \___//_/     (_)

-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
"""
)
