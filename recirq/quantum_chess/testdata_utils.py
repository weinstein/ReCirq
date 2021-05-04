import os

from typing import List, Dict

from recirq.quantum_chess.move import Move
from recirq.quantum_chess.bit_utils import squares_to_bitboard


# Standard chess board initial setup
STANDARD_SETUP_SQUARES = [f'{f}{r}' for f in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h') for r in (1, 2, 7, 8)]
STANDARD_SETUP_BITBOARD = squares_to_bitboard(STANDARD_SETUP_SQUARES)

def _read_move_list_file(game_file_path: str) -> List[Move]:
    """ Reads a list of Move strings from the given file. """
    with open(game_file_path, 'r') as handle:
        contents = handle.read().splitlines()
    return list(Move.from_string(line) for line in contents)

def _load_all_game_files() -> Dict[str, List[Move]]:
    """
    Reads all game files in the testdata directory.

    Returns a dictionary of the move lists keyed by file name.
    """
    testdata = os.path.join(os.path.dirname(__file__), 'testdata')
    ret = {}
    for f in os.listdir(testdata):
        name = os.path.splitext(f)[0]
        moves = _read_move_list_file(os.path.join(testdata, f))
        ret[name] = moves
    return ret

# The dictionary of all games in the testdata directory.
# Keys are the file name, values are the move list.
#
# For example, to write tests parameterized on these games:
# @pytest.mark.parametrize('moves',
#                          ALL_GAMES.values(),
#                          ids=ALL_GAMES.keys())
# def test_foo(moves):
#     ...
ALL_GAMES = _load_all_game_files()

# A smaller subset of ALL_GAMES that have 20 or fewer moves.
TINY_GAMES = dict((name, moves) for (name, moves) in ALL_GAMES.items() if len(moves) <= 20)
