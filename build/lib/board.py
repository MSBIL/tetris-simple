from dataclasses import dataclass, field
from typing import Optional
import json
from src.bag import Bag
from src.piece import Piece
with open('./conf/conf.json', 'r') as file:
    game_config = json.load(file)



@dataclass(init=False)
class Board:
    """
    Board represents tetris board
    pieces_table keeps track of each piece in the game
    pieces_table is aligned by rows on first axis (x)
    and by columns on second axis(y)
    Bag object (as a game code) is required to initialize and play a game
    Board can iterate through a list of Bag objects
    or a single Bag object, and
    play tetris game and output score(s)
    """
    columns: int
    rows: int
    pieces_table: list[list[int]] = field(default_factory=list)
    bag: Optional[Bag] = None
    num_removed_rows: Optional[int] = 0
    game_scores: Optional[list[int]] = field(default_factory=list)

    def __init__(self, columns, rows, bag=None):
        self.columns = columns
        self.rows = rows
        self.pieces_table = [[0 for i in range(columns)] for j in range(rows)]
        self.bag = bag

    def _reset_table(self) -> None:
        """
        Reset pieces table with zeros
        :return: None, resets pieces_table to starting position
        """
        self.pieces_table = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.num_removed_rows = 0

    def play_multi_game(self, input_file: list[str]) -> list[int]:
        """
        Play game from an input file
        :param input_file: str, path to game file
        :return: list[int]: list of scores
        """
        bag_codes = input_file
        self.game_scores = []
        for bag_code in bag_codes:
            self.play_one_game(bag_code)
            game_score = self.get_score()
            self.game_scores.append(game_score)
        return self.game_scores

    def load_input(self, input_file) -> None:
        """
        Reads input_file and converts into list of game codes
        :param input_file: str, path to input file
        :return: list of game codes, e.g. ['I0,I4', 'Q4']
        """
        with open(input_file, 'r') as f:
            game_codes = f.readlines()
        game_codes = [game_code.strip() for game_code in game_codes]
        return game_codes

    def play_one_game(self, bag_code: str) -> int:
        """
        Play game from a given bag code
        :param bag_code: str, string representing list of pieces for a game
        :return: score of game, int
        """
        self.bag = Bag(bag_code)
        self._reset_table()
        piece_iterator = iter(self.bag.get_pieces())
        done_play = False
        while not done_play:
            try:
                piece = next(piece_iterator)
            except StopIteration:
                done_play = True
            else:
                self._play_one_piece(piece)
        score = self.get_score()
        return score

    def print_game_scores(self):
        """
        Prints list of game scores
        :return: None
        """
        print('\n'.join([str(score) for score in self.game_scores]))

    def print_score(self):
        """
        Prints game score
        :return: None
        """
        print(str(self.get_score()))

    def _play_one_piece(self, piece: Piece) -> None:
        """
        Moves a piece down and updates table
        :param piece: Piece, represents current piece board is playing
        :return: None, updates board state after piece is played
        """
        if self._move_one_piece(piece):
            self._update_table()

    def get_current_state(self):
        """
        Returns current state of board
        :return: str, current non-empty rows and cols in string format
        """
        non_empty_cols = self.get_non_empty_cols()
        non_empty_rows = self.get_non_empty_rows()
        return f"non-empty rows and cols are {non_empty_rows} and {non_empty_cols}"

    def _move_one_piece(self, piece) -> bool:
        """
        Play one piece by dropping it vertically from first position on board
        :param piece: Piece, represents current piece board is playing
        :return: bool: true if can be placed on board and can be moved down
        """
        return self._place_piece(piece) and self.drop_piece_fully(piece)

    def _place_piece(self, piece) -> bool:
        """
        Tries to place a piece onto the board and returns success
        :param piece: Piece, represents current piece board is playing
        :return: bool: true if a piece can be placed on board
        """
        coords = piece.get_piece_coords()
        if any(x < 0 or x >= self.rows or y < 0 or y >= self.columns or self.pieces_table[x][y] != 0 for x, y in coords):
            return False
        for coord in coords:
            x,y = coord
            #self.pieces_table[x][y] = piece.shape.code
            self.pieces_table[x][y] = 1
        return True

    def can_move_piece(self, piece: Piece, dir_x: int, dir_y: int) -> bool:
        """
        Returns true if the piece does not intersect with
        a non-empty cell when moved
        :param piece: Piece, represents current piece board is playing
        :param dir_x: int, vertical direction, changes rows
        :param dir_y: int, horizontal direction, changes columns
        :return: bool: successful if no empty cells are moved
        """
        for x, y in piece.get_piece_coords():
            next_x = x + dir_x
            next_y = y + dir_y
            if next_x < 0 or next_x >= self.rows or next_y < 0 or next_y >= self.columns:
                return False
            if self.pieces_table[next_x][next_y] != 0:
                return False
        return True

    def drop_piece_fully(self, piece):
        """
        Drops the current piece as far down as possible and returns success
        :param piece: Piece, represents current piece board is playing
        :return: bool: true if piece can be placed on board after vertical drop
        """
        while self.can_move_piece(piece, 1, 0):
            piece.move(1, 0)
        return self._place_piece(piece)

    def _update_table(self) -> None:
        """
        Checks if a row is full and updates state of piece_table
        and increases number of removed rows count
        :return: None, updates internal state after each piece played
        """
        for y in range(self.rows):
            if self.is_row_full(y):
                self.remove_row(y)
                self._increase_removed_count()

    def _increase_removed_count(self) -> None:
        """
        Increases number of removed rows by one
        :return: None
        """
        self.num_removed_rows += 1

    def is_col_non_empty(self, y) -> bool:
        """
        Returns if column y is non-empty
        :param y: int, column number
        :return: bool
        """
        return any(self.pieces_table[x][y] != 0 for x in range(self.rows))

    def is_row_non_empty(self, x) -> bool:
        """
        Returns if row x is non-empty
        :param x: int, row number
        :return: bool
        """
        return any(self.pieces_table[x][y] != 0 for y in range(self.columns))

    def is_row_full(self, x) -> bool:
        """
        Returns if the row x is full
        :param x: int, row number
        :return: bool
        """
        return 0 not in self.pieces_table[x]

    def remove_row(self, x) -> list[int]:
        """
        Removes row x from the board and replaces with an empty row at top
        :param x: int, row number
        :return: list[int], removed row
        """
        removed_row = self.pieces_table.pop(x)
        empty_row = [0 for i in range(self.columns)]
        self.pieces_table.insert(0, empty_row)
        return removed_row

    def get_non_empty_rows(self) -> list[int]:
        """
        Finds list of non-empty rows on game boards
        :return: list[int], list of non-empty rows on game board
        """
        return list(filter(lambda x: self.is_row_non_empty(x), range(self.rows)))

    def get_non_empty_cols(self) -> list[int]:
        """
        Finds list of non-empty columns on game boards
        :return: list[int], list of non-empty rows on game board
        """
        return list(filter(lambda y: self.is_col_non_empty(y), range(self.columns)))

    def get_cleared_rows(self) -> int:
        """
        Returns the number of rows cleared during a game
        :return: int, number of cleared rows so far
        """
        return self.num_removed_rows

    def get_score(self) -> int:
        """
        Returns the score of game as defined by maximum height
        :return: int, score based on maximum height of column
        """
        return self.get_max_height()

    def get_max_height(self) -> int:
        """
        Returns the maximum height column after iterating through all columns
        :return: int, maximum column height
        """
        max_height = 0
        for y in range(self.columns):
            for x in range(self.rows):
                if self.pieces_table[x][y] != 0:
                    max_height = max(max_height, self.rows - x)
                    break
        return max_height

    def draw_board(self) -> None:
        """
        Utility to function to draw current state of board
        :return: None
        """
        for x in range(self.rows):
            row_str = []
            for y in range(self.columns):
                if self.pieces_table[x][y] != 0:
                    row_str.append(self.pieces_table[x][y])
                else:
                    row_str.append('')
            print(','.join([val for val in row_str])+'\n')
