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


@pytest.mark.parametrize('moves',
                         testdata.ALL_GAMES.values(),
                         ids=testdata.ALL_GAMES.keys())
def test_move_parsing_roundtrip(moves):
    for m in moves:
        move_str = m.to_string(include_type=True)
        assert move.Move.from_string(move_str) == m
