import random
import os
import time
import datetime
import gspread
from google.oauth2.service_account import Credentials
from game_extras import GameColours as C
from game_extras import typewriter
import game_art


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
        time.sleep(1)
        print(C.Y + "\n--------+-------+--------")
        for row in self.board:
            print(C.Y + "|       |       |       |")
            print(C.Y + "|  ", row[0], C.Y + "  |  ",
                  row[1], C.Y + "  |  ", row[2], C.Y + "  | ")
            print(C.Y + "|       |       |       |")
            print(C.Y + "--------+-------+--------")

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
        self.player1 = C.G + "X"
        self.player2 = C.R + "O"
        self.board = Board()
        self.is_computer_player = False
        self.round_count = 1
        self.score_player1 = 0
        self.score_player2 = 0

    def choose_player(self):
        """
        Ask user if the game is going to be played against the computer,
        or against a second human player. Return True or False.
        """
        player = ""
        typewriter(
            "Would you like to play against a friend or the computer?\n")
        while True:
            player = input(C.Y + "\nEnter computer or human: ")
            if player not in {"computer", "human"}:
                print(C.M + "\nOopsi! Wrong entry.")
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
        Selecte a a random first player and call play_game.
        """
        print(game_art.LOGO)
        print(game_art.GAME_RULES)
        self.is_computer_player = self.choose_player()
        print(
            C.RE + f"\nYour are Player 1 and your symbol is {self.player1}.\n")
        print(f"Player2's symbole is {self.player2}.\n")
        player = self.random_first_player()
        typewriter("Who goes first? Let's flip a coin.\n")
        typewriter(".....\n")
        time.sleep(2)
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
        Run the game loop.
        Request either the human player or the computer to make a move.
        Display the respective move on the board.
        Afterwards, verify if a move has led to a win and,
        if necessary, update the score and start a new game round.
        If not, change the player for the following move.
        Start a new round once there are no more moves left.
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
                time.sleep(2)
                return self.reset_game()
            player = self.switch_player(player)
        if num == 0:
            print(C.Y + "\nROUND OVER! IT'S A TIE!")
            time.sleep(2)
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
                move = int(input(C.Y + "Enter your move: "))
                if move > 0 and move < 10:
                    if self.board.is_field_free(move):
                        break
                    print(C.M + "\nField is taken! Please choose another one.\n")
                else:
                    print(C.M + "\nPlease enter a valid number between 1-9.\n")
            except ValueError:
                print(C.M + "\nPlease enter a valid number between 1-9.\n")
        return move

    def get_computer_move(self):
        """
        Returns a random move for the computer.
        Afterwards, check if the move can be returned,
        or if the field is taken.
        """
        print(f"\n{self.player2}! Computer's turn!\n")
        typewriter("Computer is thinking\n")
        time.sleep(2)
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
        print(C.Y + f"\nYEAH! {player} WON! CONGRATS!\n")

    def switch_player(self, player):
        """
        Switch current player to get the move from the next player
        """
        return self.player1 if player == self.player2 else self.player2

    def display_score(self):
        """
        Show the current score
        """
        print(game_art.SCORE)
        print(C. Y +
              f"\t{self.player1} = {self.score_player1}\n"
              f"\n\t{self.player2} = {self.score_player2}"
              )

    def reset_game(self):
        """
        Reset the game to play another round
        """
        self.clear()
        if self.round_count == 3:
            return self.game_over()
        self.round_count += 1
        self.display_score()
        print(game_art.NEXT_ROUND)
        typewriter(f"Are you ready for round {self.round_count}?\n")
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

        winner = (
            self.player1 if self.score_player1 > self.score_player2 else self.player2
        )
        self.display_score()
        print(game_art.GAME_OVER)
        if self.score_player1 == self.score_player2:
            return print(C.Y + "It is a tie. Thank you for playing!")
        print(f"{winner} won! Congratulations!\n")
        if self.is_computer_player:
            score = self.score_player1
        else:
            score = max(self.score_player1, self.score_player2)
        name = input(
            C.Y +
            f"Make your mark on our leaderboard. {winner} enter your name: ")
        self.update_worksheet(name, score)
        self.display_leaderboard()

    def update_worksheet(self, name, score):
        """
        Update a new row in the Tic Tact Toe worksheet
        This updates a new row with the name, score and date.
        """
        typewriter("\nUpdating Leaderboard...")
        leaderboard.append_row(
            [name, score, today_date])
        typewriter("\nLeaderboard Update successful.\n")

    def display_leaderboard(self):
        """
        Displays to the players the 15 best scores
        """
        score_sheet = SHEET.worksheet("leaderboard").get_all_values()[1:]

        sorted_data = sorted(
            score_sheet, key=lambda x: int(x[1]), reverse=True)
        count = min(len(sorted_data), 15)
        print(game_art.LEADERBOARD)

        for i, col in enumerate(sorted_data[:count], start=1):
            print(
                f"{i: >2}{col[0]: >20}{col[1]: >20}{col[2]: >20}".format(*col))


if __name__ == "__main__":
    Game().start_game()
