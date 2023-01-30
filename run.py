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
                if player == self.player1:
                    self.score_player1 += 1
                else:
                    self.score_player2 += 1
                print(f"\nYeah! {player} won! Congrats!\n")
                return self.reset_game()
            else:
                player = self.switch_player(player)
        if num == 0:
            print("Game over! It's a tie!")
            return self.reset_game()

    def get_human_player_move(self):
        """
        Get move from human player.
        Afterwards, check if the move can be returned,
        or if the field is taken.
        """
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

    def reset_game(self):
        """
        Reset the game to play another round
        """
        self.clear()
        self.round_count += 1
        while self.round_count < 3:
            print(
                f"\tPlayer 1 = {self.score_player1}\n"
                f"\n\tPlayer 2 = {self.score_player2}"
            )
            print(self.round_count)

            self.board.reset_board()
            self.board.display_board()
            player = self.random_first_player()
            self.play_game(player)
        self.game_over()

    def clear(self):
        """
        Clear terminal
        """
        os.system("cls" if os.name == "nt" else "clear")

    def game_over(self):
        """
        End of the game. Show final result.
        """
        self.clear()
        print(
            f"Game Over.\nPlayer 1 = {self.score_player1} - Player 2 = {self.score_player2}"
        )
        if self.is_computer_player:
            name = input("Player please enter your name")
            score = self.score_player1
        else:
            name = input("Player please enter your name")
            score = max(self.score_player1, self.score_player2)
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
        for data in score_sheet:
            data[1] = (data[1])

        update_data = sorted(
            score_sheet, key=lambda x: int(x[1]), reverse=True)
        print("update data")
        if (len(update_data) < 15):
            count = len(update_data)
        else:
            count = 15

        for i in range(0, count):
            print(f"""
            {i+1}\t{update_data[i][0]}\t  {update_data[i][1]}\t{
            update_data[i][2]}""")


if __name__ == "__main__":
    Game().start_game()
