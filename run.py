class Board:
    """Represents the board for the Tic-Tac-Toe game"""

    def __init__(self):
        """Initializes a new board."""
        self.board = [[i + j for i in range(1, 4)] for j in range(0, 9, 3)]

    def display_board(self):
        """
        Create the grid for the game
        """
        print("--------+-------+--------")
        for row in self.board:
            print("|       |       |       |")
            print("|  ", row[0], "  |  ", row[1], "  |  ", row[2], "  | ")
            print("|       |       |       |")
            print("--------+-------+--------")


class Game:
    """Represents a Tic-Tac-Toe game."""

    def __init__(self):
        """Initilize 2 Players and one Board."""
        self.player1 = "X"
        self.player2 = "O"
        self.board = Board()
        self.is_computer_player = False

    def choose_player(self):
        """
        Ask user if the game is going to be played against the computer,
        or against a second human player
        """
        player = ""
        print("Would you like to play against a friend or the computer?\n")
        while True:
            player = input("Enter computer or human: ")
            if player not in {"computer", "human"}:
                print("\nOopsi! Wrong entry.")
                continue
            break
        if player.lower() == "computer":
            return True
        else:
            return False


if __name__ == "__main__":
    Game().choose_player()
