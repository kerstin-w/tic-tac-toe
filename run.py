import random


class Board:
    """Represents the board for the Tic-Tac-Toe game."""

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

    def start_game(self):
        """
        Start the game with asking user to play against a computer or
        a human player.
        """
        self.is_computer_player = self.choose_player()
        print(f"Your are Player 1 and your symbol is {self.player1}.\n")
        print(f"Player2's symbole is {self.player2}.\n")
        player = self.random_first_player()
        print("Who goes first? Let's flip a coin.\n")
        print(".....\n")
        print(f"\n{player} goes first!\n")
        self.board.display_board()
        self.play_game(player)

    def random_first_player(self):
        """
        Get a random first player for the first move in the game
        """
        player = random.choice([self.player1, self.player2])
        return player

    def play_game(self, player):
        """
        Run game
        """
        if player == self.player1:
            print(f"\n{self.player1}! Your turn!\n")
        elif player == self.player2:
            if self.is_computer_player:
                print(f"\n{self.player2}! Player 2's turn!\n")
                print("Computer is thinking\n")
            else:
                print(f"\n{self.player2}! Player 2's turn!\n")


if __name__ == "__main__":
    Game().start_game()
