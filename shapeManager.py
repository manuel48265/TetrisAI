import random
import pieceForm
from collections import deque

class ShapeManager:
    """
    A class to manage the generation and manipulation of Tetris game pieces.

    Attributes:
        num_pieces (int): The total number of available Tetris piece types.
        pieces (list): A list of `pieceForm` objects representing the different Tetris shapes.

    Methods:
        get_random_piece() -> pieceForm:
            Returns a randomly selected Tetris piece from the list.

        init_rand_vector(num_elements: int) -> list:
            Generates a list of `num_elements` randomly selected Tetris pieces.
    """

    def __init__(self, num_pieces: int, pieces: list) -> None:
        """
        Initializes a ShapeManager object.

        Args:
            num_pieces (int): The total number of available Tetris piece types.
            pieces (list): A list of `pieceForm` objects representing the different Tetris shapes.
        """
        self.num_pieces = num_pieces
        self.pieces = pieces

    def get_random_piece(self) -> pieceForm:
        """
        Returns a randomly selected Tetris piece from the list.

        Returns:
            pieceForm: A randomly chosen Tetris piece.
        """
        return random.choice(self.pieces)

    def init_rand_deque(self, num_elements: int) -> deque:
        """
        Generates a list of `num_elements` randomly selected Tetris pieces.

        Args:
            num_elements (int): The number of pieces to include in the generated list.

        Returns:
            list: A list of `num_elements` randomly chosen Tetris pieces.
        """
        output = deque()
        for i in range(num_elements):
            output.append(self.get_random_piece())
        return output