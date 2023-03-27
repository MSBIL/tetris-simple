import unittest

from src.board import Board

class BoardTest(unittest.TestCase):
    '''
    Unit test for board class
    '''

    def setUp(self):
        """ Initializes board and couple of games and their expected results"""
        self.board = Board(10, 100)
        self.valid_game_to_bag_code_map = {
                                            'game1': 'I0,I4,Q8',
                                            'game2': 'T1,Z3,I4',
                                            'game3': 'Q0,I2,I6,I0,I6,I6,Q2,Q4',
                                          }
        self.valid_game_expected_results_map = {
                                                'game1': {'score': 1, 'nonempty_cols': 2, 'nonempty_rows': 1,
                                                          'cleared_rows': 1},
                                                'game2': {'score': 4, 'nonempty_cols': 7, 'nonempty_rows': 4,
                                                          'cleared_rows': 0},
                                                'game3': {'score': 3, 'nonempty_cols': 10, 'nonempty_rows': 3,
                                                          'cleared_rows': 2},
                                                }

    def test_has_correct_width(self):
        """Tests width of board"""
        self.assertEqual(self.board.columns, 10)

    def test_has_correct_height(self):
        """Tests height of board"""
        self.assertEqual(self.board.rows, 100)

    def test_play_valid_games(self):
        """Tests game results for each test game by comparing scores, number of non-empty columns, number of non-empty rows, and total number of cleared rows"""
        for game_code,bag_code in self.valid_game_to_bag_code_map.items():
            self.board.play_one_game(bag_code)
            game_score = self.board.get_score()
            game_non_empty_cols = len(self.board.get_non_empty_cols())
            game_non_empty_rows = len(self.board.get_non_empty_rows())
            game_cleared_rows = self.board.get_cleared_rows()
            expected_score = self.valid_game_expected_results_map[game_code]['score']
            expected_non_empty_cols = self.valid_game_expected_results_map[game_code]['nonempty_cols']
            expected_non_empty_rows = self.valid_game_expected_results_map[game_code]['nonempty_rows']
            expected_cleared_rows = self.valid_game_expected_results_map[game_code]['cleared_rows']
            self.assertEqual(game_score, expected_score)
            self.assertEqual(game_non_empty_cols, expected_non_empty_cols)
            self.assertEqual(game_non_empty_rows, expected_non_empty_rows)
            self.assertEqual(game_cleared_rows, expected_cleared_rows)