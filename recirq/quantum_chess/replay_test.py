import pytest
import cirq
import os
import sys
from typing import List

import recirq.engine_utils as utils
import recirq.quantum_chess.bit_utils as u
import recirq.quantum_chess.enums as enums
import recirq.quantum_chess.move as move
import recirq.quantum_chess.quantum_board as qb
import recirq.quantum_chess.testdata_utils as testdata


CIRQ_BOARDS = {
    'default': qb.CirqBoard(0, error_mitigation=enums.ErrorMitigation.Error),
    'Syc54-noiseless': qb.CirqBoard(0,
                 device=utils.get_device_obj_by_name('Syc54-noiseless'),
                 error_mitigation=enums.ErrorMitigation.Error),
    'Syc23-noiseless': qb.CirqBoard(0,
                 device=utils.get_device_obj_by_name('Syc23-noiseless'),
                 error_mitigation=enums.ErrorMitigation.Error),
    'Syc23-simulator': qb.CirqBoard(0,
                 sampler=utils.get_sampler_by_name('Syc23-simulator'),
                 device=utils.get_device_obj_by_name('Syc23-simulator'),
                 error_mitigation=enums.ErrorMitigation.Correct,
                 noise_mitigation=0.10),
    # 'weber': qb.CirqBoard(0, sampler=utils.get_sampler_by_name('Sycamore54', gateset='sqrt-iswap'),
    #                device=utils.get_device_obj_by_name('Sycamore54'),
    #                error_mitigation=enums.ErrorMitigation.Correct,
    #                noise_mitigation=0.10),
}

@pytest.mark.parametrize('moves',
                         testdata.ALL_GAMES.values(),
                         ids=testdata.ALL_GAMES.keys())
def test_move_parsing_roundtrip(moves):
    for m in moves:
        move_str = m.to_string(include_type=True)
        assert move.Move.from_string(move_str) == m

@pytest.mark.parametrize('board', CIRQ_BOARDS.values(), ids=CIRQ_BOARDS.keys())
@pytest.mark.parametrize('moves',
                         testdata.ALL_GAMES.values(),
                         ids=testdata.ALL_GAMES.keys())
def test_game_replay(board, moves, request):
    print(f'running {request.node.callspec.id}')
    b = board.with_state(testdata.STANDARD_SETUP_BITBOARD)
    for move in moves:
        print(f'move: {move.to_string(include_type=True)}')
        b.do_move(move)
        b.sample(100)

