import sys
import json
with open('./conf/conf.json', 'r') as file:
    game_config = json.load(file)
from src.board import Board

def play_tetris_from_stdin(input_file):
    """Run file version of tetris"""
    play_from_file(input_file)

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

def parse_stdin() -> list[str]:
    """
    Parses stdin into a list of strings
    :return:
    """
    stdin_input = []
    for line in sys.stdin:
        stdin_input.append(line)
    return stdin_input


def tetris():
    """
    Entry script for tetris game, it can be either played from an input file with multi-games or a single game with a game code
    """
    stdin_args = parse_stdin()
    play_tetris_from_stdin(stdin_args)

if __name__ == '__main__':
    tetris()
