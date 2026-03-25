# Author: Chanse Syres
# GitHub username: chansesyres
# Date: 06/11/2023
# Description: This code runs a game called Othello.

# How to play?
# Enter "othello.py" in the terminal, it will launch the game.
# Rules: https://www.eothello.com/#how-to-play

# game = Othello()
# game.create_player("Alice", "black")
# game.create_player("Bob", "white")
# game.play_game()

class Player:
    """Represents a player participating in the game."""
    def __init__(self, player_name, piece_color):
        """Creates and stores the players name and color for the game."""
        self._player_name = player_name
        self._piece_color = piece_color

    def get_name(self):
        return self._player_name

    def get_color(self):
        return self._piece_color

    def set_name(self, name):
        self._player_name = name

    def set_color(self, color):
        self._piece_color = color

class Othello:
    """Represents the game board and the rules of the Othello game."""
    def __init__(self):
        """Initializes a game board and prepares it for a new game."""
        self._board = [['*' for _ in range(10)] for _ in range(10)]
        for i in range(1, 9):
            for j in range(1, 9):
                self._board[i][j] = '.'
        self._board[4][4] = 'O'
        self._board[5][5] = 'O'
        self._board[4][5] = 'X'
        self._board[5][4] = 'X'
        self._players = []

    def print_board(self):
        """Prints the current state of the game board object."""
        print("  " + " ".join(str(i) for i in range(1, 9)))
        for idx, row in enumerate(self._board[1:9], 1):
            print(f"{idx} " + " ".join(row[1:9]))

    def create_player(self, player_name, color):
        """Creates a player object with a given name and piece color (black or white) and adds it to the game."""
        if color.lower() not in ["black", "white"]:
            print("Invalid color. Choose between black and white.")
        elif len(self._players) >= 2:
            print("Cannot add more than two players.")
        else:
            new_player = Player(player_name, color.lower())
            if color.lower() == "black":
                self._players.insert(0, new_player)
            else:
                self._players.append(new_player)

    def return_winner(self):
        """Determines and returns the winner of the game or declares it a draw."""
        white_count = sum(row.count('O') for row in self._board)
        black_count = sum(row.count('X') for row in self._board)
        if white_count > black_count:
            return f"Winner is white player: {self._players[0].get_name() if self._players[0].get_color() == 'white' else self._players[1].get_name()}"
        elif black_count > white_count:
            return f"Winner is black player: {self._players[0].get_name() if self._players[0].get_color() == 'black' else self._players[1].get_name()}"
        else:
            return "The game is a draw"

    def _valid_move(self, color, row, col):
        """Checks if a move is valid for a color at a particular position."""
        if self._board[row][col] != '.' or not self._on_board(row, col):
            return False
        opponent = 'O' if color == 'X' else 'X'
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            r, c = row + dr, col + dc
            if self._on_board(r, c) and self._board[r][c] == opponent:
                while self._on_board(r, c) and self._board[r][c] == opponent:
                    r += dr
                    c += dc
                if self._on_board(r, c) and self._board[r][c] == color:
                    return True
        return False

    def _on_board(self, row, col):
        """Verifies if a position is within the game board object boundaries."""
        return 1 <= row <= 8 and 1 <= col <= 8

    def return_available_positions(self, color):
        """Returns a list of all available positions for a given color and where a valid move can be made."""
        available_positions = []
        for i in range(1, 9):
            for j in range(1, 9):
                if self._valid_move(color, i, j):
                    available_positions.append((i, j))
        return available_positions

    def make_move(self, color, piece_position):
        """Places a piece at a specific position and flips any opponent pieces in ordinance with the game rules."""
        piece_color = 'X' if color == 'black' else 'O'
        if not self._valid_move(piece_color, piece_position[0], piece_position[1]):
            return False
        self._board[piece_position[0]][piece_position[1]] = piece_color
        opponent = 'O' if piece_color == 'X' else 'X'
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            r, c = piece_position[0] + dr, piece_position[1] + dc
            pieces_to_flip = []
            while self._on_board(r, c) and self._board[r][c] == opponent:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            if self._on_board(r, c) and self._board[r][c] == piece_color:
                for rf, cf in pieces_to_flip:
                    self._board[rf][cf] = piece_color
        return True

    def play_game(self):
        """Conducts the entire gameplay. Handles player turns, receives input, makes moves, and announces the winner"""
        player_colors = ['black', 'white']
        player_index = 0
        while True:
            player_color = player_colors[player_index]
            piece_color = 'X' if player_color == 'black' else 'O'
            available_moves = self.return_available_positions(piece_color)
            self.print_board()
            if not available_moves:
                other_piece_color = 'O' if piece_color == 'X' else 'X'
                if not self.return_available_positions(other_piece_color):
                    break
                print(f"No available moves for {self._players[player_index].get_name()}. Skipping turn.")
                player_index = 1 - player_index
                continue
            print(f"Player: {self._players[player_index].get_name()} ({player_color})")
            print("Available moves: ", available_moves)
            while True:
                try:
                    row = int(input("Enter the row (1-8): "))
                    col = int(input("Enter the column (1-8): "))
                    if (row, col) in available_moves:
                        self.make_move(player_color, (row, col))
                        break
                    else:
                        print("Invalid move. Please choose one from the list of available moves.")
                except ValueError:
                    print("Invalid input. Please enter integers for row and column.")
            player_index = 1 - player_index
        self.print_board()
        print(self.return_winner())

if __name__ == "__main__":
    game = Othello()
    game.create_player("Alice", "black")
    game.create_player("Bob", "white")
    game.play_game()