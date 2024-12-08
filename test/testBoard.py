import pytest
import copy
from src.board import Board
from src.piece import Piece
import src.utils.pieceForm as pf


grid_0 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
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
    """Tests if the piece is within the grid's valid boundaries.
    
    Args:
        piece (Piece): The piece to be tested.
        width (int): The width of the board.
        height (int): The height of the board.
        target (bool): The expected result (True if valid, False if out of bounds).
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
    """Tests if the piece collides with existing blocks or boundaries.
    
    Args:
        piece (Piece): The piece to be tested.
        grid (list of list of int): The current state of the board.
        target (bool): The expected result (True if no collision, False otherwise).
    """
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
    """ Test the _cols_down method of the Board class.
    
    Args:
        grid (list of list of int): The current state of the board.
        lines (list of int): The lines to be removed.
        target_grid (list of list of int): The expected result after removing the lines.
    """
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)
    test_board._cols_down(lines)

    assert test_board.grid == target_grid

@pytest.mark.parametrize(
    "piece,grid,target",
    [
        (Piece(0, 0, pf.PIECE_I), grid_3, True),
        (Piece(0, 0, pf.PIECE_Z), grid_3, False),
        (Piece(0, 0, pf.PIECE_L), grid_3, False),
        (Piece(0, 0, pf.PIECE_J), grid_3, False),
        (Piece(0, 0, pf.PIECE_L), grid_1, True),
        (Piece(0, 0, pf.PIECE_J), grid_1, True),
        (Piece(0, 0, pf.PIECE_I), grid_1, True)
    ],
)
def test_set_new_piece(piece,grid,target):
    """ Test the set_new_piece method of the Board class.
    
    Args:
        piece (Piece): The piece to be set.
        grid (list of list of int): The current state of the board.
        target (bool): The expected result after setting the piece.
    """
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    assert test_board.set_new_piece(copy.deepcopy(piece)) == target


@pytest.mark.parametrize(
    "piece,grid,rotate_state,target",
    [
        (Piece(-1, 0, pf.PIECE_I), grid_0, 3, True),
        (Piece(-1, 0, pf.PIECE_Z), grid_0, 1, True),
        (Piece(0, 0, pf.PIECE_Z), grid_4, 0, False),
        (Piece(0, 0, pf.PIECE_S), grid_1, 0, False),
        (Piece(4, 0, pf.PIECE_I), grid_0, 3, True)
    ],
)
def test_rotate_piece(piece,grid,rotate_state,target):
    """ Test the rotate_piece method of the Board class.
    
    Args:
        piece (Piece): The piece to be rotated.
        grid (list of list of int): The current state of the board.
        rotate_state (int): The number of times the piece should be rotated.
        target (bool): The expected result after rotating the piece.
    """
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)
    
    for i in range(rotate_state):
        piece.rotate()

    test_board.current_piece = piece

    assert test_board.rotate_piece() == target

#
@pytest.mark.parametrize(
    "piece,grid,rotate_state,target",
    [
        (Piece(0, -1, pf.PIECE_I), grid_1, 0, True),
        (Piece(0, 0, pf.PIECE_I), grid_1, 0, False),
        (Piece(0, 0, pf.PIECE_L), grid_4, 0, False),
        (Piece(0, 0, pf.PIECE_J), grid_0, 0, True),
        (Piece(0, 4, pf.PIECE_L), grid_0, 0, False),
        (Piece(0, 3, pf.PIECE_T), grid_0, 2, False),
        (Piece(0, 0, pf.PIECE_I), grid_0, 1, True)
    ],
)
def test_move_piece_down(piece,grid,rotate_state,target):
    """
    Test the move_piece_down method of the Board class.

    Args:
        piece (Piece): The piece to be moved.
        grid (list of list of int): The current state of the board.
        rotate_state (int): The number of times the piece should be rotated.
        target (bool): The expected result after moving the piece down.
    
    """
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    for i in range(rotate_state):
        piece.rotate()

    test_board.current_piece = piece

    assert test_board.move_piece_down() == target

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
def test_move_piece_right(piece,grid,target):
    """
    Test the move_piece_right method of the Board class.

    Args:
        piece (Piece): The piece to be moved.
        grid (list of list of int): The current state of the board.
        target (bool): The expected result after moving the piece right.
    """
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    test_board.current_piece = piece

    if not target:
        pair = (test_board.current_piece.x,test_board.current_piece.y)
        assert pair == (piece.x,piece.y)
    assert test_board.move_piece_right() == target

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
    """ Test the move_piece_left method of the Board class.
    
    Args:
        piece (Piece): The piece to be moved.
        grid (list of list of int): The current state of the board.
        target (bool): The expected result after moving the piece left.
    """
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    test_board.current_piece = copy.deepcopy(piece)

    if not target:
        pair = (test_board.current_piece.x,test_board.current_piece.y)
        assert pair == (piece.x,piece.y)
    assert test_board.move_piece_left() == target
    
# TODO
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
    """
        Test the identify_lines method of the Board class.

            grid (list of list of int): The grid representing the current state of the board.
            lines (list of int): The lines to be identified.
            target (list of int): The expected result after identifying the lines.

        Asserts:
            The result of identify_lines method matches the target.
    """
    test_board = Board(len(grid[0]),len(grid))
    test_board.grid = copy.deepcopy(grid)

    assert test_board.identify_lines(lines) == target 

@pytest.mark.parametrize(
    "grid,target_metrics",
    [
        # Test Case 0: Grid Vacío
        (
            grid_0,
            {
                'holes': 0,
                'max_height': 0,
                'avg_height': 0.0,
                'height_diff': 0.0
            }
        ),
        # Test Case 1: Filas Completamente Llenas
        (
            grid_1,
            {
                'holes': 0,
                'max_height': 4,          # Altura máxima de las filas llenas
                'avg_height': 4.0,     # 4 columnas * altura 4
                'height_diff': 0.0         # Todas las columnas tienen la misma altura
            }
        ),
        # Test Case 2: Filas Alternadas Llenas y Vacías sin Huecos
        (
            grid_2,
            {
                'holes': 15,
                'max_height': 6,          # Altura máxima de las filas llenas
                'avg_height': 6.0,     # 5 columnas * altura 6
                'height_diff': 0.0         # Todas las columnas tienen la misma altura
            }
        ),
        # Test Case 3: Filas Llenas con Huecos en Columnas Específicas
        (
            grid_3,
            {
                'holes': 11,                # Huecos en dos columnas
                'max_height': 6,           # Altura máxima de las filas llenas
                'avg_height': 6.0,      # 5 columnas * altura 6
                'height_diff': 0.0          # Todas las columnas tienen la misma altura
            }
        ),
        # Test Case 4: Alturas Desiguales con Múltiples Huecos
        (
            grid_4,
            {
                'holes': 9,                # Huecos distribuidos en varias columnas
                'max_height': 7,           # Altura máxima en alguna columna
                'avg_height': 5.6,      # Suma de las alturas de todas las columnas
                'height_diff': 4.0          # Diferencia total entre alturas de columnas adyacentes
            }
        ),
    ],
)
def test_get_metrics(grid, target_metrics):
    """
    Test the get_metrics method of the Board class. 

    Args:
        grid (list of list of int): The grid representing the current state of the board.
        target_metrics (dict): The expected metrics of the board.
    """
    width = len(grid[0])
    height = len(grid)
    test_board = Board(width, height)
    test_board.grid = copy.deepcopy(grid)
    
    metrics = test_board.get_metrics()

    EPSILON = 1e-6
    assert abs(metrics['avg_height'] - target_metrics['avg_height']) < EPSILON
    assert metrics['holes'] == target_metrics['holes']
    assert metrics['max_height'] == target_metrics['max_height']
    assert metrics['height_diff'] == target_metrics['height_diff']

