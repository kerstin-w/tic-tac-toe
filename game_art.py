"""
ASCII art to illustrate the game better
"""
from game_extras import GameColours as C


# Logo for the start of the game

LOGO = C.M + r'''
-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-

     ______  ____   __      ______   ____    __      ______   ___     ___
    |      ||    | /  ]    |      | /    |  /  ]    |      | /   \   /  _]
    |      | |  | /  /     |      ||  o  | /  /     |      ||     | /  [_
    |_|  |_| |  |/  /      |_|  |_||     |/  /      |_|  |_||  O  ||    _]
      |  |   |  /   \_       |  |  |  _  /   \_       |  |  |     ||   [_
      |  |   |  \     |      |  |  |  |  \     |      |  |  |     ||     |
      |__|  |____\____|      |__|  |__|__|\____|      |__|   \___/ |_____|


-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-O-X-
'''
# Rules of the game

GAME_RULES = C.Y + r'''
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

'''
