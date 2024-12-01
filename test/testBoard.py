import pytest
import copy
from src.board import Board
from src.piece import Piece
import src.pieceForm as pf


grid_1 = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
]

grid_2 =[
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0]
]

grid_3 =[
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0]
]

grid_4 =[
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0]
]

grid_5 =[
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0]
]

grid_1_result =[
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

grid_3_result =[
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 0, 0]
]

grid_4_result =[
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 1, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 0, 0]
]



@pytest.mark.parametrize(
    "piece,width,heigth,target",
    [
        (Piece(9, 10, pf.PIECE_I), 10, 20, False),
        (Piece(-1, 10, pf.PIECE_I), 10, 20, False),
        (Piece(9, -1, pf.PIECE_I), 10, 20, False),
        (Piece(9, 22, pf.PIECE_I), 10, 20, False),
        (Piece(4, 7, pf.PIECE_I), 10, 20, True)
    ],
)
def test_out_of_limits(piece,width,heigth,target):
    """AI is creating summary for test_out_of_limits

    Args:
        piece ([type]): [description]
        width ([type]): [description]
        heigth ([type]): [description]
        target ([type]): [description]
    """
    test_board = Board(width,heigth)
    test_board.current_piece = piece

    assert test_board.is_valid_position() == target
@pytest.mark.parametrize(
    "piece,grid,target",
    [
        (Piece(0, 0, pf.PIECE_I), grid_3, False),
        (Piece(0, 1, pf.PIECE_I), grid_3, True),
        (Piece(0, 0, pf.PIECE_O), grid_4, True),
        (Piece(0, 0, pf.PIECE_Z), grid_4, True),
        (Piece(1, 1, pf.PIECE_Z), grid_4, False)
    ],
)
def test_piece_colide(piece,grid,target):
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    test_board.current_piece = piece

    assert test_board.is_valid_position() == target
@pytest.mark.parametrize(
    "grid,lines,target_grid",
    [
        (grid_1,[2,3,4,5],grid_1_result),
        (grid_3,[1,3,5],grid_3_result),
        (grid_4,[3,5],grid_4_result)
    ],
)
def test_cols_down(grid,lines,target_grid):
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    test_board._cols_down(lines) == target_grid

def test_set_new_piece():
    pass

def test_rotate_piece():
    pass

def test_move_piece_down():
    pass

@pytest.mark.parametrize(
    "piece,grid,target",
    [
        (Piece(0, 0, pf.PIECE_I), grid_2, False),
        (Piece(0, 1, pf.PIECE_I), grid_3, True),
        (Piece(0, 0, pf.PIECE_O), grid_4, False),
        (Piece(1, 0, pf.PIECE_Z), grid_5, True),
        (Piece(1, 1, pf.PIECE_Z), grid_5, False)
    ]
)
def test_move_piece_rigth(piece,grid,target):
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    test_board.current_piece = piece

    if not target:
        pair = (test_board.current_piece.x,test_board.current_piece.y)
        assert pair == (piece.x,piece.y)
    assert test_board.move_piece_rigth() == target

@pytest.mark.parametrize(
    "piece,grid,target",
    [
        (Piece(0, 0, pf.PIECE_I), grid_2, False),
        (Piece(1, 1, pf.PIECE_I), grid_3, True),
        (Piece(0, 0, pf.PIECE_O), grid_4, False),
        (Piece(1, 0, pf.PIECE_Z), grid_5, True),
        (Piece(1, 1, pf.PIECE_Z), grid_5, True)
    ]
)
def test_move_piece_left(piece,grid,target):
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    test_board.current_piece = copy.deepcopy(piece)

    if not target:
        pair = (test_board.current_piece.x,test_board.current_piece.y)
        assert pair == (piece.x,piece.y)
    assert test_board.move_piece_left() == target
    

def test_lock_piece():
    pass

@pytest.mark.parametrize(
    "grid,lines,target",
    [
        (grid_1, [0, 1, 2, 3, 4, 5], [2, 3, 4, 5]),
        (grid_2, [0, 1, 2, 3, 4, 5], [1, 3, 5])
    ]
)
def test_identify_lines(grid,lines,target):
    """AI is creating summary for test_identify_lines

    Args:
        grid ([type]): [description]
        lines ([type]): [description]
        target ([type]): [description]
    """
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    assert test_board.identify_lines(lines) == target 

