import unittest

from src.piece import Piece
from src.shape import Shape

class PieceTest(unittest.TestCase):
    '''
    Unit test for piece class
    '''

    def setUp(self):
        self.valid_piece_codes = ['Q', 'Z', 'S', 'T', 'I', 'L', 'J']
        self.pieces_to_expected_origin_map = {'Q': [(0,0),(0,1),(1,0),(1,1)],
                                            'Z': [(0,0),(0,1),(1,1),(1,2)],
                                            'S': [(0,1),(0,2),(1,0),(1,1)],
                                            'T': [(0,0),(0,1),(0,2),(1,1)],
                                            'I': [(0,0),(0,1),(0,2),(0,3)],
                                            'L': [(0,0),(1,0),(2,0),(2,1)],
                                            'J': [(0,1),(1,1),(2,0),(2,1)],
                                            'V': None
                                            }
        self.pieces_to_expected_after_move_map = {'Q': [(1,0),(1,1),(2,0),(2,1)],
                                            'Z': [(1,0),(1,1),(2,1),(2,2)],
                                            'S': [(1,1),(1,2),(2,0),(2,1)],
                                            'T': [(1,0),(1,1),(1,2),(2,1)],
                                            'I': [(1,0),(1,1),(1,2),(1,3)],
                                            'L': [(1,0),(2,0),(3,0),(3,1)],
                                            'J': [(1,1),(2,1),(3,0),(3,1)],
                                            'V': None
                                            }

    def test_pieces_at_origin(self):
        """ Testing pieces at origin, should get no error"""
        for piece_code in self.valid_piece_codes:
            my_shape = Shape(piece_code)
            my_piece = Piece(0, 0, my_shape)
            my_piece.initialize_coords()
            expected_coords = set(self.pieces_to_expected_origin_map.get(piece_code))
            self.assertSetEqual(my_piece.get_piece_coords(), expected_coords)

    def test_pieces_after_move_one_unit_down(self):
        """ Testing pieces after moving one unit down from origin, should get no error"""
        for piece_code in self.valid_piece_codes:
            my_shape = Shape(piece_code)
            my_piece = Piece(0, 0, my_shape)
            my_piece.move(1, 0)
            expected_coords = set(self.pieces_to_expected_after_move_map.get(piece_code))
            self.assertSetEqual(my_piece.get_piece_coords(), expected_coords)