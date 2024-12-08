import pytest
from src.utils.pieceForm import PieceForm  # Adjust the module name based on your project structure.

@pytest.mark.parametrize(
    "matrix, expected_rotation",
    [
        ([[1, 0], [0, 1]], [[0, 1], [1, 0]]),  # Basic test for a 2x2 matrix.
        ([[1, 1, 0], [0, 1, 0], [0, 1, 1]], [[0, 0, 1], [1, 1, 1], [1, 0, 0]]),  # Test for a 3x3 matrix.
        ([[1, 0, 0], [1, 1, 0], [0, 0, 1]], [[0, 1, 1], [0, 1, 0], [1, 0, 0]]),  # Another test for a 3x3 matrix.
    ],
)
def test_rotate(matrix, expected_rotation):
    """
    Test to verify that the rotation of a piece works correctly.

    This test ensures that a piece, represented by its matrix, rotates 90 degrees clockwise.
    The test passes if the resulting matrix after rotation matches the expected matrix.

    Parameters:
    - matrix: The initial matrix of the piece.
    - expected_rotation: The matrix that is expected after rotation.
    """
    piece = PieceForm(matrix, color=1)  # Create a PieceForm object with the given matrix.
    piece.rotate()  # Rotate the piece.
    assert piece.matrix == expected_rotation  # Verify that the rotated matrix matches the expected one.


@pytest.mark.parametrize(
    "matrix, expected_unrotation",
    [
        ([[0, 1], [1, 0]], [[1, 0], [0, 1]]),  # Test to undo rotation on a 2x2 matrix.
        ([[0, 0, 1], [1, 1, 1], [1, 0, 0]], [[1, 1, 0], [0, 1, 0], [0, 1, 1]]),  # Undo rotation on a 3x3 matrix.
        ([[0, 1, 0], [0, 1, 1], [1, 0, 0]], [[0, 1, 0], [1, 1, 0], [0, 0, 1]]),  # Another test to undo rotation on a 3x3 matrix.
    ],
)
def test_unrotate(matrix, expected_unrotation):
    """
    Test to verify that the unrotation (counterclockwise rotation) works correctly.

    This test ensures that a piece, represented by its matrix, undoes a previous 90-degree clockwise 
    rotation. The test passes if the resulting matrix after unrotation matches the expected matrix.

    Parameters:
    - matrix: The initial matrix of the piece.
    - expected_unrotation: The matrix that is expected after undoing the rotation.
    """
    piece = PieceForm(matrix, color=1)  # Create a PieceForm object with the given matrix.
    piece.unrotate()  # Undo the rotation of the piece.
    assert piece.matrix == expected_unrotation  # Verify that the resulting matrix matches the expected one.


@pytest.mark.parametrize(
    "matrix, expected_repr",
    [
        ([[1, 0], [0, 1]], "1 0\n0 1"),  # Test the string representation of a 2x2 matrix.
        ([[1, 1, 1], [0, 0, 1], [1, 0, 0]], "1 1 1\n0 0 1\n1 0 0"),  # Test the string representation of a 3x3 matrix.
    ],
)
def test_repr(matrix, expected_repr):
    """
    Test to verify that the string representation of a piece is correct.

    This test ensures that the __repr__ method of the PieceForm class outputs a string that 
    correctly represents the piece's matrix.

    Parameters:
    - matrix: The matrix of the piece.
    - expected_repr: The expected string representation of the piece.
    """
    piece = PieceForm(matrix, color=1)  # Create a PieceForm object with the given matrix.
    assert repr(piece) == expected_repr  # Verify that the string representation matches the expected one.


@pytest.mark.parametrize(
    "matrix, color, expected_color",
    [
        ([[1, 0], [0, 1]], 5, 5),  # Test color assignment and retrieval.
        ([[1, 1, 1], [0, 0, 1], [1, 0, 0]], 3, 3),  # Another test for color assignment.
    ],
)
def test_get_color(matrix, color, expected_color):
    """
    Test to verify that the assigned color of a piece is correctly returned.

    This test ensures that the color assigned to a PieceForm object is the same as the color retrieved
    using the get_color method.

    Parameters:
    - matrix: The matrix of the piece.
    - color: The color to assign to the piece.
    - expected_color: The expected color after assignment.
    """
    piece = PieceForm(matrix, color=color)  # Create a PieceForm object with the given matrix and color.
    assert piece.get_color() == expected_color  # Verify that the returned color matches the expected one.

