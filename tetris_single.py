import argparse
import sys
import json
with open('./conf/conf.json', 'r') as file:
    game_config = json.load(file)
from src.board import Board

def play_tetris_from_args(input_file, game_code):
    """Run either file version or game code version of tetris"""
    if input_file is not None:
        play_from_file(input_file)
    if game_code is not None:
        play_from_code(game_code)

def play_from_file(input):
    """
    Play from a well-conditioned input file as described in project requirements
    An input is a list of game codes seperated by new line
    A code is a comma seperated list of two character strings, first character is any valid shape (Q,Z,S,T,I,L,J)
    and second character denoting the starting column on the board
    """
    board_width = game_config['board_shapes']['width']
    board_height = game_config['board_shapes']['height']
    tetris_board = Board(board_width, board_height)
    tetris_board.play_multi_game(input)
    tetris_board.print_game_scores()

def play_from_code(code):
    """
    Play from a well-conditioned game code as described in project requirements
    A code is a comma seperated list of two character strings, first character is any valid shape (Q,Z,S,T,I,L,J)
    and second character denoting the starting column on the board
    :arg
    code: str
    """
    board_width = game_config['board_shapes']['width']
    board_height = game_config['board_shapes']['height']
    tetris_board = Board(board_width, board_height)
    tetris_board.play_one_game(code)
    tetris_board.print_score()

def tetris():
    """
    Entry script for tetris game, it can be either played from an input file with multi-games or a single game with a game code
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("input", help="Input file to games", type=str, nargs="?")
    group.add_argument("-i", help="Input file to games", type=str)
    group.add_argument("-g", "--game", help="String representation of a game", type=str)
    args = parser.parse_args()
    play_tetris_from_args(args.i, args.game)

if __name__ == '__main__':
    tetris()
