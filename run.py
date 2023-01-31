import random
import os
import datetime
import gspread
from google.oauth2.service_account import Credentials


# Import date from datetime
date = datetime.datetime.today()
today_date = date.strftime("%d/%m/%Y")

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("tictactoe")

leaderboard = SHEET.worksheet("leaderboard")

data = leaderboard.get_all_values()


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
        row, column = self.get_index(position)
        self.board[row][column] = player

    def get_index(self, position):
        """
        Convert player move into row and column on the grid
        """
        return (int((position - 1) / 3), int((position - 1) % 3))

    def is_field_free(self, move):
        """
        Check if the choosen field is not occupied
        """
        row, column = self.get_index(move)
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
        if (
            self.board[0][2]
            == self.board[1][1]
            == self.board[2][0]
            == player
        ):
            return True

    def reset_board(self):
        """
        Reset the board for a new round of the game
        """
        Board.__init__(self)


class Game:
    """Represents a Tic-Tac-Toe game."""

    def __init__(self):
        """Initilize 2 Players and one Board."""
        self.player1 = "X"
        self.player2 = "O"
        self.board = Board()
        self.is_computer_player = False
        self.round_count = 1
        self.score_player1 = 0
        self.score_player2 = 0

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
        return random.choice([self.player1, self.player2])

    def play_game(self, player):
        """
        Run game
        """
        num = 9
        while num > 0:
            num -= 1
            if player == self.player1:
                position = self.get_human_player_move(player)
            elif player == self.player2:
                if self.is_computer_player:
                    position = self.get_computer_move()
                else:
                    position = self.get_human_player_move(player)
            self.board.make_move(position, player)
            self.board.display_board()
            if self.board.check_winner(player):
                self.update_score(player)
                return self.reset_game()
            player = self.switch_player(player)
        if num == 0:
            print("Game over! It's a tie!")
            return self.reset_game()

    def get_human_player_move(self, player):
        """
        Get move from human player.
        Afterwards, check if the move can be returned,
        or if the field is taken.
        """
        print(f"\n{player}! Your turn!\n")
        while True:
            try:
                move = int(input("Enter your move: "))
                if move > 0 and move < 10:
                    if self.board.is_field_free(move):
                        break
                    print("Field is taken! Please choose another one.\n")
                else:
                    print("\nPlease enter a valid number between 1-9.\n")
            except ValueError:
                print("\nPlease enter a valid number between 1-9.\n")
        return move

    def get_computer_move(self):
        """
        Returns a random move for the computer.
        Afterwards, check if the move can be returned,
        or if the field is taken.
        """
        print(f"\n{self.player2}! Computer's turn!\n")
        print("Computer is thinking\n")
        while True:
            move = random.randint(1, 9)
            if self.board.is_field_free(move):
                break
        return move

    def update_score(self, player):
        """
        Update Player score once a round is won
        """
        if player == self.player1:
            self.score_player1 += 1
        else:
            self.score_player2 += 1
        print(f"\nYeah! {player} won! Congrats!\n")

    def switch_player(self, player):
        """
        Switch current player to get the move from the next player
        """
        return self.player1 if player == self.player2 else self.player2

    def reset_game(self):
        """
        Reset the game to play another round
        """
        self.clear()
        if self.round_count == 3:
            return self.game_over()

        print(
            f"\tPlayer 1 = {self.score_player1}\n"
            f"\n\tPlayer 2 = {self.score_player2}"
        )
        self.round_count += 1
        print(self.round_count)
        self.board.reset_board()
        self.board.display_board()
        player = self.random_first_player()
        self.play_game(player)
        return None

    def clear(self):
        """
        Clear terminal
        """
        os.system("cls" if os.name == "nt" else "clear")

    def game_over(self):
        """
        End of the game. Show final result.
        """
        print(
            f"Game Over.\nPlayer 1 = {self.score_player1} - Player 2 = {self.score_player2}"
        )
        if self.is_computer_player:
            score = self.score_player1
        else:
            score = max(self.score_player1, self.score_player2)
        name = input("Player please enter your name")
        self.update_worksheet(name, score)
        self.display_leaderboard()

    def update_worksheet(self, name, score):
        """
        Update a new row in the Tic Tact Toe worksheet
        This updates a new row with the name, score and date.
        """
        print("Updating Leaderboard...\n")
        leaderboard.append_row(
            [name, score, today_date])
        print("Leaderboard Update successful.\n")

    def display_leaderboard(self):
        """
        Displays to the players the 15 best scores
        """
        score_sheet = SHEET.worksheet("leaderboard").get_all_values()[1:]
        sorted_data = sorted(
            score_sheet, key=lambda x: int(x[1]), reverse=True)
        count = min(len(sorted_data), 15)

        for i, col in enumerate(sorted_data[:count], start=1):
            print(f"{i}\t{col[0]}\t{col[1]}\t{col[2]}")


if __name__ == "__main__":
    Game().start_game()
