import unittest
from src.bag import Bag

class BagTest(unittest.TestCase):
    '''
    Unit test for bag class
    '''

    def setUp(self):
        self.valid_piece_codes = ['Q', 'Z', 'S', 'T', 'I', 'L', 'J']
        self.inputs_expected_to_fail = ['',
                                        'Q,Q1',
                                        'I5,8'
                                        ]
        self.inputs_expected_to_pass = ['Q0',
                                        'Q0,Q1',
                                        'I0,I4,Q8',
                                        'I0,I4,Q8,I0,I4',
                                        'L0,Z2,S4,T6,J8'
                                        ]
        self.expected_position_for_pass_inputs = [ [set([(0,0),(0,1),(1,0),(1,1)])],
                                                   [set([(0, 0), (0, 1), (1, 0), (1, 1)]),
                                                    set([(0, 1), (0, 2), (1, 1), (1, 2)])],
                                                   [set([(0, 0), (0, 1), (0, 2), (0, 3)]),
                                                    set([(0, 4), (0, 5), (0, 6), (0, 7)]),
                                                    set([(0, 8), (0, 9), (1, 8), (1, 9)])],
                                                   [set([(0, 0), (0, 1), (0, 2), (0, 3)]),
                                                    set([(0, 4), (0, 5), (0, 6), (0, 7)]),
                                                    set([(0, 8), (0, 9), (1, 8), (1, 9)]),
                                                    set([(0, 0), (0, 1), (0, 2), (0, 3)]),
                                                    set([(0, 4), (0, 5), (0, 6), (0, 7)])],
                                                   [set([(0, 0), (1, 0), (2, 0), (2, 1)]),
                                                    set([(0, 2), (0, 3), (1, 3), (1, 4)]),
                                                    set([(0, 5), (0, 6), (1, 4), (1, 5)]),
                                                    set([(0, 6), (0, 7), (0, 8), (1, 7)]),
                                                    set([(0, 9), (1, 9), (2, 8), (2, 9)])]
                                                  ]

    def test_valid_inputs(self):
        """ Testing bag with valid inputs, should get no error"""
        for i,bag_code in enumerate(self.inputs_expected_to_pass):
            my_bag = Bag(bag_code)
            my_coords = my_bag.get_pieces_coords()
            expected_coords = self.expected_position_for_pass_inputs[i]
            self.assertListEqual(my_coords, expected_coords)

    def test_invalid_inputs(self):
        """ Testing bag with invalid inputs, should get an error"""
        for i,bag_code in enumerate(self.inputs_expected_to_fail):
            with self.assertRaises(Exception) as context:
                my_bag = Bag(bag_code)
                my_coords = my_bag.get_pieces_coords()
            self.assertTrue('Bag code is not valid' in str(context.exception))