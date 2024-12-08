import pytest
from src.piece import Piece
import numpy as np
import src.utils.pieceForm as pf

@pytest.mark.parametrize(
    "pos_x, pos_y",
    [
        (5, 4),      # Standard valid position
        (3, 6),      # Another standard valid position
        (0, 0),      # Origin position
        (-1, 5),     # Negative X-coordinate
        (7, -2),     # Negative Y-coordinate
        (10, 10),    # Position outside typical grid bounds
    ],
)
def test_set_position(pos_x, pos_y):
    """Tests the correct assignment of X and Y positions when creating a Piece.
    
    Args:
        pos_x (int): The X-coordinate for the piece's position.
        pos_y (int): The Y-coordinate for the piece's position.
    """
    piece = Piece(pos_x, pos_y)

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
    """ Tests the correct identification of empty rows in a piece.
    
    Args:
        piece (Piece): The piece to check for empty rows.
        target (list): The expected results for each row.
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
    """Tests the correct retrieval of the vertical lines occupied by a piece.

    Args:
        piece (Piece): The piece to check for vertical lines.
        posx (int): The X-coordinate for the piece's position.
        posy (int): The Y-coordinate for the piece's position.
        target (list): The expected results for the vertical lines.
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
    """Tests the correct adjustment of a piece's position to stay within the horizontal bounds.

    Args:
        piece (Piece): The piece to adjust.
        posx (int): The X-coordinate for the piece's position.
        sizex (int): The maximum horizontal size of the board.
        target (int): The expected X-coordinate after adjustment.
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
    """Tests the correct update of the game grid with the piece's shape.
    
    Args:
        initial_pos (tuple): The initial position of the piece.
        expected_grid (np.array): The expected game grid after updating with the piece's shape.
    """
    piece = Piece(initial_pos[0],initial_pos[1], pf.PIECE_Z)
    grid = np.zeros((4, 4), dtype=int)
    piece.into_numpy(grid)
    np.testing.assert_array_equal(grid, expected_grid)

