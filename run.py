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

    def make_move(self, position, player):
        """
        Add current move to the grid
        """
        row = self.get_row_index(position)
        column = self.get_col_index(position)
        self.board[row][column] = player

    def get_row_index(self, position):
        """
        Convert user input to row in the grid
        """
        return int((position - 1) / 3)

    def get_col_index(self, position):
        """
        Convert user input to cell in the grid
        """
        return int((position - 1) % 3)

    def is_field_free(self, move):
        """
        Check if the choosen field is not occupied
        """
        row = self.get_row_index(move)
        column = self.get_col_index(move)
        if not isinstance(self.board[row][column], int):
            return False
        return True

    def check_winner(self, player):
        """
        Check for a winner in rows, columns and diagonals.
        Also check if the grid is full and there is a tie.
        """
        # check in rows
        for row in self.board:
            board_items = set(row)
            if len(board_items) == 1 and (not isinstance(board_items, int)):
                return True

        # check in columns
        for i in range(3):
            if (
                self.board[0][i]
                == self.board[1][i]
                == self.board[2][i]
                == player
            ):
                return True

        # check in diagonals
        if (
            self.board[0][0]
            == self.board[1][1]
            == self.board[2][2]
            == player
        ):
            return True
        elif (
            self.board[0][2]
            == self.board[1][1]
            == self.board[2][0]
            == player
        ):
            return True


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
        num = 9
        while num > 0:
            num -= 1
            if player == self.player1:
                print(f"\n{self.player1}! Your turn!\n")
                position = self.get_human_player_move()
            elif player == self.player2:
                print(f"\n{self.player2}! Player 2's turn!\n")
                if self.is_computer_player:
                    print("Computer is thinking\n")
                    position = self.get_computer_move()
                else:
                    position = self.get_human_player_move()
            self.board.make_move(position, player)
            self.board.display_board()

            if self.board.check_winner(player):
                print(f"\nYeah! {player} won! Congrats!\n")
            else:
                player = self.switch_player(player)
        if num == 0:
            print("Game over! It's a tie!")

    def get_human_player_move(self):
        """
        Get move from human player.
        Afterwards, check if the move can be returned,
        or if the field is taken.
        """
        while True:
            move = int(input("Enter your move: "))
            if self.board.is_field_free(move):
                break
            else:
                print(
                    "\nField is taken! Please choose another one.\n")
        return move

    def get_computer_move(self):
        """
        Returns a random move for the computer.
        Afterwards, check if the move can be returned,
        or if the field is taken.
        """
        while True:
            move = random.randint(1, 9)
            if self.board.is_field_free(move):
                break
        return move

    def switch_player(self, player):
        """
        Switch current player to get the move from the next player
        """
        player = self.player1 if player == self.player2 else self.player2
        return player


if __name__ == "__main__":
    Game().start_game()
