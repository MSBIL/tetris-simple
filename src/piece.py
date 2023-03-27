"""
Piece Class
"""
from dataclasses import dataclass, field
from src.shape import Shape


@dataclass(init=True)
class Piece:
    """
    Piece represents each piece in tetris game
    It has a Shape object inside and its x,y coordinates
    move operation can be called to change location of a Piece
    """
    x: int
    y: int
    shape: Shape
    piece_coords: list[(int, int)] = field(default_factory=list)

    def initialize_coords(self) -> None:
        """
        Initialize piece coordinates
        if piece_coords is None, get_piece_coords updates it
        :return: None
        """
        self.piece_coords = None
        self.piece_coords = self.get_piece_coords()

    def move(self, x, y) -> None:
        """
        Move the piece by x amount in row
        and y amount in column
        After move piece_coords is set to None
        to update coordinates after move
        :param x: int, vertical direction
        :param y: int, horizontal direction
        :return:
        """
        self.x += x
        self.y += y
        self.piece_coords = None

    def get_piece_coords(self) -> set[(int, int)]:
        """
        Returns a list of coordinates that the piece occupies
        :return: set[int], set of piece coordinates
        """
        if self.piece_coords is None:
            begin_x = self.x
            begin_y = self.y
            shape_coords = self.shape.get_shape_coords()
            self.piece_coords = set([(begin_x + offset_x, begin_y + offset_y) for offset_x, offset_y in shape_coords])
        return self.piece_coords
