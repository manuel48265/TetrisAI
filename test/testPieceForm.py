import pytest
from src.pieceForm import PieceForm  # Adjust the module name based on your project structure.

@pytest.mark.parametrize(
    "matrix, expected_rotation",
    [
        ([[1, 0], [0, 1]], [[0, 1], [1, 0]]),  # Basic 2x2 matrix.
        ([[1, 1, 0], [0, 1, 0], [0, 1, 1]], [[0, 0, 1], [1, 1, 1], [1, 0, 0]]),  # 3x3 matrix.
        ([[1, 0, 0], [1, 1, 0], [0, 0, 1]], [[0, 1, 1], [0, 1, 0], [1, 0, 0]]),  # Another 3x3 matrix.
    ],
)
def test_rotate(matrix, expected_rotation):
    """Tests that 90° clockwise rotation works correctly."""
    piece = PieceForm(matrix, color=1)
    piece.rotate()
    assert piece.matrix == expected_rotation


@pytest.mark.parametrize(
    "matrix, expected_unrotation",
    [
        ([[0, 1], [1, 0]], [[1, 0], [0, 1]]),  # Undo rotation on 2x2 matrix.
        ([[0, 0, 1], [1, 1, 1], [1, 0, 0]], [[1, 1, 0], [0, 1, 0], [0, 1, 1]]),  # Undo rotation on 3x3 matrix.
        ([[0, 1, 0], [0, 1, 1], [1, 0, 0]], [[0, 1, 0], [1, 1, 0], [0, 0, 1]]),  # Another 3x3 matrix.
    ],
)
def test_unrotate(matrix, expected_unrotation):
    """Tests that 90° counterclockwise rotation (undo rotation) works correctly."""
    piece = PieceForm(matrix, color=1)
    piece.unrotate()
    assert piece.matrix == expected_unrotation


@pytest.mark.parametrize(
    "matrix, expected_repr",
    [
        ([[1, 0], [0, 1]], "1 0\n0 1"),  # 2x2 matrix string representation.
        ([[1, 1, 1], [0, 0, 1], [1, 0, 0]], "1 1 1\n0 0 1\n1 0 0"),  # 3x3 matrix.
    ],
)
def test_repr(matrix, expected_repr):
    """Tests the string representation of the matrix."""
    piece = PieceForm(matrix, color=1)
    assert repr(piece) == expected_repr


@pytest.mark.parametrize(
    "matrix, color, expected_color",
    [
        ([[1, 0], [0, 1]], 5, 5),  # Test color assignment.
        ([[1, 1, 1], [0, 0, 1], [1, 0, 0]], 3, 3),  # Another color.
    ],
)
def test_get_color(matrix, color, expected_color):
    """Tests that the correct color is returned."""
    piece = PieceForm(matrix, color=color)
    assert piece.get_color() == expected_color
