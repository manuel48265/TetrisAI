import pytest
from src.piece import Piece
import numpy as np
import src.utils.pieceForm as pf

@pytest.mark.parametrize(
    "pos_x,pos_y",
    [
        (5,4),
        (3,6)
    ],
)
def test_set_position(pos_x,pos_y):
    """AI is creating summary for test_set_position

    Args:
        pos_x ([type]): [description]
        pos_y ([type]): [description]
    """
    piece = Piece(pos_x,pos_y)

    assert (piece.x == pos_x and piece.y == pos_y)

@pytest.mark.parametrize(
    "piece,target",
    [
        (pf.PIECE_I, [True,False,True,True]),
        (pf.PIECE_L, [False,False,True]),
        (pf.PIECE_Z, [False, False, True])
    ],
)
def test_is_empty_row(piece,target):
    """AI is creating summary for test_is_empty_row

    Args:
        piece ([type]): [description]
        target ([type]): [description]
    """
    test_piece = Piece(0,0,piece)
    output =[]
    for i in range(test_piece.size()):
        output.append(test_piece.is_empty_row(i))

    assert output == target

@pytest.mark.parametrize(
    "piece,posx,posy,target",
    [
        (pf.PIECE_I,3,4,[4,5,6,7]),
        (pf.PIECE_I,3,2,[2,3,4,5]),
        (pf.PIECE_O,3,7,[7,8]),
    ],
)
def test_get_lines(piece,posx,posy,target):
    """AI is creating summary for test_get_lines

    Args:
        piece ([type]): [description]
        posx ([type]): [description]
        posy ([type]): [description]
        target ([type]): [description]
    """
    test_piece = Piece(posx,posy,piece)
    output= test_piece.get_lines()

    assert output == target

@pytest.mark.parametrize(
    "piece,posx,sizex,target",
    [
        (pf.PIECE_I,-2,5,0),
        (pf.PIECE_I,20,5,1),
        (pf.PIECE_O,3,10,3),
    ],
)
def test_adjust_pos(piece,posx,sizex,target):
    """AI is creating summary for test_adjust_pos

    Args:
        piece ([type]): [description]
        posx ([type]): [description]
        sizex ([type]): [description]
        target ([type]): [description]
    """
    test_piece = Piece(posx,0,piece)

    test_piece.adjust_pos(sizex)

    assert test_piece.x == target

@pytest.mark.parametrize("initial_pos, expected_grid", [
    ((0, 0), np.array([
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])),
    ((1, 1), np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 0]
    ])),
    ((1, 2), np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1]
    ]))
])
def test_into_numpy(initial_pos, expected_grid):
    piece = Piece(initial_pos[0],initial_pos[1], pf.PIECE_Z)
    grid = np.zeros((4, 4), dtype=int)
    piece.into_numpy(grid)
    np.testing.assert_array_equal(grid, expected_grid)

