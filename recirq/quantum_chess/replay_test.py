import pytest
import cirq
import os
from typing import List

import recirq.engine_utils as utils
import recirq.quantum_chess.bit_utils as u
import recirq.quantum_chess.enums as enums
import recirq.quantum_chess.move as move
import recirq.quantum_chess.quantum_board as qb
import recirq.quantum_chess.testdata_utils as testdata


ALL_CIRQ_BOARDS = [
    qb.CirqBoard(0, error_mitigation=enums.ErrorMitigation.Error),
    qb.CirqBoard(0,
                 device=utils.get_device_obj_by_name('Syc54-noiseless'),
                 error_mitigation=enums.ErrorMitigation.Error),
    qb.CirqBoard(0,
                 device=utils.get_device_obj_by_name('Syc23-noiseless'),
                 error_mitigation=enums.ErrorMitigation.Error),
    qb.CirqBoard(0,
                 sampler=utils.get_sampler_by_name('Syc23-simulator-tester'),
                 device=utils.get_device_obj_by_name('Syc23-simulator-tester'),
                 error_mitigation=enums.ErrorMitigation.Correct,
                 noise_mitigation=0.10),
]

@pytest.mark.parametrize('moves',
                         testdata.ALL_GAMES.values(),
                         ids=testdata.ALL_GAMES.keys())
def test_move_parsing_roundtrip(moves):
    for m in moves:
        move_str = m.to_string(include_type=True)
        assert move.Move.from_string(move_str) == m

@pytest.mark.parametrize('board', ALL_CIRQ_BOARDS)
@pytest.mark.parametrize('moves',
                         testdata.TINY_GAMES.values(),
                         ids=testdata.TINY_GAMES.keys())
def test_tiny_replay(board, moves):
    b = board.with_state(testdata.STANDARD_SETUP_BITBOARD)
    for move in moves:
        print(f'move: {move.to_string(include_type=True)}')
        b.do_move(move)
        b.sample(100)
