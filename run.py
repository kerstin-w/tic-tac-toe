import random
import time
import datetime
import gspread
from google.oauth2.service_account import Credentials
from game_extras import GameColours as Colors
from game_extras import typewriter
from game_extras import input_with_validation
import game_art


# Import date from datetime
date = datetime.datetime.today()
today_date = date.strftime("%d/%m/%Y")

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("tictactoe")

leaderboard = SHEET.worksheet("leaderboard")


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
        print(Colors.Y + "\n--------+-------+--------")
        for row in self.board:
            print(Colors.Y + "|       |       |       |")
            print(
                Colors.Y + "|  ",
                row[0],
                Colors.Y + "  |  ",
                row[1],
                Colors.Y + "  |  ",
                row[2],
                Colors.Y + "  | ",
            )
            print(Colors.Y + "|       |       |       |")
            print(Colors.Y + "--------+-------+--------")

    def make_move(self, position, player_symbol):
        """
        Add current move to the grid
        """
        row, column = self.get_row_column_index(position)
        self.board[row][column] = player_symbol

    def get_row_column_index(self, position):
        """
        Convert player move into row and column on the grid
        """
        return (int((position - 1) / 3), int((position - 1) % 3))

    def is_field_free(self, selected_position):
        """
        Check if the choosen field is not occupied.
        """
        row, column = self.get_row_column_index(selected_position)
        if not isinstance(self.board[row][column], int):
            return False
        return True

    def check_winner(self, player_symbol):
        """
        Check for a winner in rows, columns and diagonals.
        """
        # check in rows
        for row in self.board:
            board_items = set(row)
            # Length 1 means all the elements in the row are same
            if len(board_items) == 1 and (not isinstance(board_items, int)):
                return True

        # check in columns
        for i in range(3):
            if (
                self.board[0][i]
                == self.board[1][i]
                == self.board[2][i]
                == player_symbol
            ):
                return True

        # check in diagonals
        if (
            self.board[0][0]
            == self.board[1][1]
            == self.board[2][2]
            == player_symbol
        ):
            return True
        if (
            self.board[0][2]
            == self.board[1][1]
            == self.board[2][0]
            == player_symbol
        ):
            return True
        return None

    def reset_board(self):
        """
        Reset the board for a new round of the game
        """
        Board.__init__(self)


class Game:
    """
    Represents the complete gameplay
    """

    # Consts to be used for the game
    MAX_GRID_CELLS = 9
    NO_OF_ROUNDS = 5

    def __init__(self):
        """
        Initilize 2 Player, the Board, wether computer is a palyer,
        the round round and player scores.
        """
        self.player1 = Colors.G + "X"
        self.player2 = Colors.R + "O"
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
            "Would you like to play against a friend or the computer?\n"
        )

        player = input_with_validation(
            prompt="\nEnter (computer/human):\n ",
            valid_options={"computer", "human"},
        )

        if player == "computer":
            self.is_computer_player = True
        return self.is_computer_player

    def start_game(self):
        """
        Start the game with asking user to play against a computer or
        a human player.
        Selecte a a random first player and call play_game.
        """
        print(game_art.GAME_RULES)
        self.choose_player()
        print(
            Colors.RE
            + f"\nYour are Player 1 and your symbol is {self.player1}.\n"
        )
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
        max_grid_cells = self.MAX_GRID_CELLS
        while max_grid_cells > 0:
            max_grid_cells -= 1
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
        if max_grid_cells == 0:
            print(Colors.Y + "\nROUND OVER! IT'S A TIE!")
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
                selected_position = int(input(Colors.Y + "Enter your move:\n"))
                if selected_position > 0 and selected_position < 10:
                    if self.board.is_field_free(selected_position):
                        break
                    print(
                        Colors.M
                        + "\nField is taken! Please choose another one.\n"
                    )
                else:
                    print(
                        Colors.M
                        + "\nPlease enter a valid number between 1-9.\n"
                    )
            except ValueError:
                print(
                    Colors.M + "\nPlease enter a valid number between 1-9.\n"
                )
        return selected_position

    def get_computer_move(self):
        """
        Returns a random move for the computer.
        Afterwards, check if the move can be returned,
        or if the field is taken.
        """
        print(f"\n{self.player2}! Computer's turn!\n")
        typewriter("Computer is thinking....\n")
        time.sleep(2)
        while True:
            selected_position = random.randint(1, 9)
            if self.board.is_field_free(selected_position):
                break
        return selected_position

    def update_score(self, player):
        """
        Update Player score once a round is won.
        """
        if player == self.player1:
            self.score_player1 += 1
        else:
            self.score_player2 += 1
        print(Colors.Y + f"\nYEAH! {player} WON! CONGRATS!\n")

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
        print(
            Colors.Y + f"\t{self.player1} = {self.score_player1}\n"
            f"\n\t{self.player2} = {self.score_player2}"
        )

    def reset_game(self):
        """
        Reset the game to play another round.
        Get a new random player and start play_game.
        Once all 5 rounds are played return game_over.
        """
        no_of_rounds = self.NO_OF_ROUNDS
        if self.round_count == no_of_rounds:
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

    def game_over(self):
        """
        End of the game.
        Compare the scores of Player 1 and Player 2 to determine the winner.
        If the scores are tied, display a tie. Players who only play against
        the Computer can enter their name and update the leadboard.
        For players playing against a human, winner is asked to enter Name and
        update the leadboard.
        """
        winner = (
            self.player1
            if self.score_player1 > self.score_player2
            else self.player2
        )
        self.display_score()
        print(game_art.GAME_OVER)
        if self.score_player1 == self.score_player2:
            print(Colors.Y + "It is a tie. Thank you for playing!")
            return
        print(f"{winner}  W O N! C O N G R A T U L A T I O N S!\n")
        if self.is_computer_player:
            score = self.score_player1
        else:
            score = max(self.score_player1, self.score_player2)
        winner_name = self.get_winner_name(winner)
        self.update_score_worksheet(winner_name, score)
        self.display_leaderboard()

    def get_winner_name(self, winner):
        """
        Ask game winner for their name. If the input is empty,
        ask for the name again.
        """
        while True:
            selected_winner_name = input(
                Colors.Y
                + f"Make your mark on our leaderboard. \
                \n{winner} enter your name:\n"
            )
            if len(selected_winner_name) == 0:
                print(Colors.M + "This is not a valid name!\n")
                continue
            break
        return selected_winner_name

    def update_score_worksheet(self, winner_name, score):
        """
        Add a new row in the Tic Tac Toe worksheet
        with the name, score and date.
        """
        typewriter("\nUpdating Leaderboard...")
        try:
            leaderboard.append_row([winner_name, score, today_date])
            typewriter("\nLeaderboard Update successful.\n")
        except (
            gspread.exceptions.GSpreadException,
            gspread.exceptions.APIError,
            gspread.exceptions.WorksheetNotFound,
        ):
            print(
                "\nWe're sorry. Something went wrong. Score was not saved."
            )

    def display_leaderboard(self):
        """
        From the score worksheet, the scores are sorted from
        highest to lowest and the top 15 scores, or less, are
        displayed.
        """
        try:
            score_sheet = SHEET.worksheet("leaderboard").get_all_values()[1:]

            sorted_data = sorted(
                score_sheet, key=lambda x: int(x[1]), reverse=True
            )
            count = min(len(sorted_data), 15)
            print(game_art.LEADERBOARD)

            for i, col in enumerate(sorted_data[:count], start=1):
                print(
                    f"{i: >2}{col[0]: >20}{col[1]: >20}{col[2]: >20}".format(
                        *col
                    )
                )
        except (
            gspread.exceptions.GSpreadException,
            gspread.exceptions.APIError,
            gspread.exceptions.WorksheetNotFound,
        ):
            print(
                "\nSomething went wrong. Leaderboard can't be shown."
            )


def display_menu():
    """
    User is asked wether to play the game, or see the leaderboard.
    """
    typewriter(
        "Would you like to start the game (g), or see the leaderboard (l)?\n"
    )
    return input_with_validation(
        prompt="\nEnter (g/l):\n", valid_options={"g", "l"}
    )


def running_game():
    """
    If the user choses to play the game, the game will start.
    Otherwise the leaderoard will be displayed with the option
    to start the game or not.
    """
    print(game_art.LOGO)
    menu_choice = display_menu()
    if menu_choice == "g":
        Game().start_game()
        return
    Game().display_leaderboard()
    typewriter("\nWould you like to start the game now?\n")
    start_game = input_with_validation(
        prompt="\nEnter (y/n):\n", valid_options={"y", "n"}
    )
    if start_game == "y":
        Game().start_game()
        return
    print("\nTHANK YOU! MAYBE NEXT TIME!")


if __name__ == "__main__":
    running_game()
