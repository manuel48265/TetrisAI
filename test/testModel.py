import pytest
from src.AI.model import CNNmodel, DQLAgent
from src.AI.preprocessing import Preprocessing
from collections import deque
from src.utils.pieceForm import pieces
from src.piece import Piece
import numpy as np
from src.board import Board

@pytest.mark.parametrize(
    "grid_shape, num_actions, num_pieces",
    [
        ((20, 10, 2), 4, 7),  # Configuración original
        ((10, 10, 1), 3, 5),  # Grid más pequeño y menos piezas
        ((30, 15, 3), 5, 10), # Grid más grande y más piezas
        ((20, 20, 2), 6, 8),  # Grid cuadrado con más acciones
        ((15, 15, 1), 4, 6),  # Grid cuadrado más pequeño
    ]
)
def test_CNNmodel(grid_shape, num_actions, num_pieces):
    model = CNNmodel(grid_shape, num_actions, num_pieces)
    assert model.grid_piece_shape == grid_shape
    assert model.num_actions == num_actions
    assert model.num_pieces == num_pieces

grid = Board(20, 10)
piece = Piece(0,0,pieces[0])
next_pieces = deque()
next_pieces.append(Piece(0,0,pieces[0]))
next_pieces.append(Piece(0,0,pieces[1]))
next_pieces.append(Piece(0,0,pieces[2]))
next_pieces_2 = deque()
next_pieces_2.append(Piece(0,0,pieces[3]))
next_pieces_2.append(Piece(0,0,pieces[4]))
next_pieces_2.append(Piece(0,0,pieces[5]))

@pytest.mark.parametrize(
    "grid, piece, next_pieces, piece_set,num_actions",
    [
        (grid, piece, next_pieces, pieces,4), # Configuración original
        (grid, piece, next_pieces_2, pieces,7)  # Configuración original
    ]
)
def test_predict(grid: Board, piece, next_pieces, piece_set,num_actions):
    preprocessing = Preprocessing(grid.get_grid(), piece, next_pieces, piece_set)

    network = CNNmodel(preprocessing.get_input_size()[0], num_actions=num_actions, num_pieces=len(piece_set))
    inputs = preprocessing.get_input()

    result = network.predict(inputs)
    assert result.shape == (num_actions,)