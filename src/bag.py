"""
Bag class
"""
from dataclasses import dataclass, field
from typing import Optional
from src.piece import Piece
from src.shape import Shape


@dataclass(init=True)
class Bag:
    """
    Bag converts a game code into list of pieces
    A game code is a list of two character strings
    of the form (ShapeCode + ColumnPosition)
    ShapeCode is a valid shape code (Q,Z,S,T,I,L,J)
    ColumnPosition is between 0-max_width of board
    A game code is a comma separated string
    some examples are: “I0,I4,Q8”, “Q4,Q8” etc
    """
    piece_str: str
    pieces: Optional[list[Piece]] = field(default_factory=list)

    def create_pieces(self) -> None:
        """
        Convert piece string to list of Piece objects
        :return: None
        """
        self.pieces = []
        piece_str_split = self.piece_str.split(',')
        for piece in piece_str_split:
            try:
                shape_code, y_coord = piece[0], piece[1]
            except IndexError as exc:
                raise Exception("Bag code is not valid") from exc
            new_piece = Piece(0, int(y_coord), Shape(shape_code))
            self.pieces.append(new_piece)

    def get_pieces(self) -> list[Piece]:
        """
        Retrieves list of pieces
        :return: list[Piece], list of piece objects
        """
        self.create_pieces()
        return self.pieces

    def get_pieces_coords(self) -> list[set[(int, int)]]:
        """
        Returns a list of piece coordinates represented in the bag
        Relative coordinates of a piece are set of integer pairs
        :return: list[set[int]]
        """
        self.create_pieces()
        piece_coords = []
        for piece in self.pieces:
            piece.initialize_coords()
            new_piece_coords = piece.get_piece_coords()
            piece_coords.append(new_piece_coords)
        return piece_coords
