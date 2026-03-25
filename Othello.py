# Author: Chanse Syres
# GitHub username: chansesyres
# Date: 06/11/2023
# Description: Console Othello game for CS 162.

# How to play?
# Enter "othello.py" in the terminal, it will launch the game.
# Rules: https://www.eothello.com/#how-to-play

# game = Othello()
# game.create_player("Alice", "black")
# game.create_player("Bob", "white")
# game.play_game()

class Player:
    """Represents a player in the Othello game."""

    def __init__(self, player_name, piece_color):
        """Initializes a player with a name and piece color."""
        self._name = player_name
        self._color = piece_color

    def get_name(self):
        """Returns the player's name."""
        return self._name

    def get_color(self):
        """Returns the player's color."""
        return self._color

    def set_name(self, name):
        """Sets the player's name."""
        self._name = name

    def set_color(self, color):
        """Sets the player's color."""
        self._color = color


class Othello:
    """Represents the Othello board and game rules."""

    _DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    def __init__(self):
        """Initializes a 10x10 board with an 8x8 area to play and two starting pieces each."""
        self._board = [['*' for _ in range(10)] for _ in range(10)]
        for row in range(1, 9):
            for col in range(1, 9):
                self._board[row][col] = '.'

        self._board[4][4] = 'O'
        self._board[4][5] = 'X'
        self._board[5][4] = 'X'
        self._board[5][5] = 'O'

        self._players = []

    def create_player(self, player_name, piece_color):
        """Creates a player object and adds it to the game."""
        normalized_color = self._normalize_player_color(piece_color)

        if len(self._players) >= 2:
            raise ValueError("Cannot add more than two players.")

        if any(player.get_color() == normalized_color for player in self._players):
            raise ValueError("Each player must have a different color.")

        new_player = Player(player_name, normalized_color)
        self._players.append(new_player)
        return new_player

    def print_board(self):
        """Prints the entire board including the boundarys of the board."""
        for row in self._board:
            print(" ".join(row))

    def return_winner(self):
        """Returns the winner of the game or a draw message."""
        black_count = sum(row.count('X') for row in self._board)
        white_count = sum(row.count('O') for row in self._board)

        if black_count > white_count:
            return f"Winner is black player: {self._get_player_name('black')}"
        if white_count > black_count:
            return f"Winner is white player: {self._get_player_name('white')}"
        return "The game is a draw"

    def return_available_positions(self, color):
        """Returns every valid move for the given color."""
        piece_symbol = self._normalize_piece_symbol(color)
        available_positions = []

        for row in range(1, 9):
            for col in range(1, 9):
                if self._captures_for_move(piece_symbol, row, col):
                    available_positions.append((row, col))

        return available_positions

    def make_move(self, color, piece_position):
        """Places a piece on the board and then flips all captured opponent pieces."""
        piece_symbol = self._normalize_piece_symbol(color)
        row, col = piece_position

        if not self._on_board(row, col):
            return False

        pieces_to_flip = self._captures_for_move(piece_symbol, row, col)
        if not pieces_to_flip:
            return False

        self._board[row][col] = piece_symbol
        for flip_row, flip_col in pieces_to_flip:
            self._board[flip_row][flip_col] = piece_symbol

        return True

    def play_game(self, player_color, piece_position):
        """
        Makes one moves for a player if the move is valid.

        Returns:
            True if the move was made successfully.
            False if the move was invalid.
            A winner/draw string if the game has ended.
        """
        player_symbol = self._normalize_piece_symbol(player_color)
        other_symbol = 'O' if player_symbol == 'X' else 'X'
        row, col = piece_position

        current_positions = self.return_available_positions(player_symbol)
        other_positions = self.return_available_positions(other_symbol)

        if not current_positions and not other_positions:
            return self.return_winner()

        if not current_positions:
            return False

        if not self._on_board(row, col):
            return False

        if self._board[row][col] != '.':
            return False

        if piece_position not in current_positions:
            return False

        self.make_move(player_symbol, piece_position)

        current_positions_after = self.return_available_positions(player_symbol)
        other_positions_after = self.return_available_positions(other_symbol)

        if not current_positions_after and not other_positions_after:
            return self.return_winner()

        return True

    def run_cli_game(self):
        """Runs the interactive terminal version of the game."""
        if len(self._players) != 2:
            raise ValueError("Creates exactly two players before starting the game.")

        current_color = 'black'

        while True:
            current_symbol = self._normalize_piece_symbol(current_color)
            other_color = 'white' if current_color == 'black' else 'black'
            other_symbol = self._normalize_piece_symbol(other_color)

            current_positions = self.return_available_positions(current_symbol)
            other_positions = self.return_available_positions(other_symbol)

            if not current_positions and not other_positions:
                break

            self.print_board()
            print()

            if not current_positions:
                print(f"{self._get_player_name(current_color)} has no valid moves. Turn skipped.")
                print()
                current_color = other_color
                continue

            print(f"Player: {self._get_player_name(current_color)} ({current_color})")
            print(f"Available moves: {current_positions}")

            result = False
            while True:
                try:
                    row = int(input("Enter row (1-8): ").strip())
                    col = int(input("Enter column (1-8): ").strip())
                except ValueError:
                    print("Invalid input. Please enter integers.")
                    continue

                result = self.play_game(current_color, (row, col))
                if result is True:
                    break

                if isinstance(result, str):
                    break

                print("Invalid move. Choose an open playable space that flips at least one piece.")

            if isinstance(result, str):
                break

            print()
            current_color = other_color

        self.print_board()
        print(self.return_winner())

    def _normalize_player_color(self, color):
        """Converts accepted player colors into stored player colors."""
        color = color.lower()
        mapping = {
            'black': 'black',
            'white': 'white',
            'b': 'black',
            'w': 'white',
            'x': 'black',
            'o': 'white'
        }

        if color not in mapping:
            raise ValueError("Color must be black, white, B, W, X, or O.")

        return mapping[color]

    def _normalize_piece_symbol(self, color):
        """Converts accepted color inputs into board symbols."""
        color = color.lower()
        mapping = {
            'black': 'X',
            'white': 'O',
            'b': 'X',
            'w': 'O',
            'x': 'X',
            'o': 'O'
        }

        if color not in mapping:
            raise ValueError("Color must be black, white, B, W, X, or O.")

        return mapping[color]

    def _on_board(self, row, col):
        """Returns True if the position is inside of the playable area."""
        return 1 <= row <= 8 and 1 <= col <= 8

    def _captures_for_move(self, piece_symbol, row, col):
        """Returns a list of opponent pieces that would be flipped by a move."""
        if not self._on_board(row, col):
            return []

        if self._board[row][col] != '.':
            return []

        opponent_symbol = 'O' if piece_symbol == 'X' else 'X'
        captured_positions = []

        for row_change, col_change in self._DIRECTIONS:
            check_row = row + row_change
            check_col = col + col_change
            directional_captures = []

            while self._on_board(check_row, check_col) and self._board[check_row][check_col] == opponent_symbol:
                directional_captures.append((check_row, check_col))
                check_row += row_change
                check_col += col_change

            if directional_captures and self._on_board(check_row, check_col) and self._board[check_row][check_col] == piece_symbol:
                captured_positions.extend(directional_captures)

        return captured_positions

    def _get_player_name(self, color):
        """Returns the name of the player with the given color."""
        normalized_color = self._normalize_player_color(color)

        for player in self._players:
            if player.get_color() == normalized_color:
                return player.get_name()

        return normalized_color


if __name__ == "__main__":
    game = Othello()

    print("Welcome to Othello!")
    black_name = input("Enter black player's name: ").strip()
    white_name = input("Enter white player's name: ").strip()

    if not black_name:
        black_name = "Black"
    if not white_name:
        white_name = "White"

    game.create_player(black_name, "black")
    game.create_player(white_name, "white")
    print()
    game.run_cli_game()
