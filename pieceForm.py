from constPieces import tetris_pieces
class PieceForm:
    def __init__(self, matrix, color) -> None:
        """
        Initializes the piece with a matrix representing its shape and a color.

        Args:
            matrix (list of list of int): A 2D square matrix representing the shape of the piece.
            color (int): An integer representing the color of the piece.

        Raises:
            ValueError: If the matrix is not square or is empty.
        """
        if not matrix or not all(len(row) == len(matrix) for row in matrix):
            raise ValueError("The matrix must be square and cannot be empty")
        
        self.matrix = matrix  # The matrix representing the shape of the piece.
        self.size = len(matrix)  # The size of the matrix (its dimension, assuming it's square).
        self.color = color  # The color associated with the piece.

    def _rotate(self, clockwise=True):
        """
        Performs an in-place rotation of the piece's matrix.

        Args:
            clockwise (bool): If True, rotates 90° clockwise. If False, rotates 90° counterclockwise.
        """
        i_limit, j_limit = self._get_limits()
        for i in range(i_limit):
            for j in range(j_limit):
                if clockwise:
                    aux = self.matrix[i][j]
                    self.matrix[i][j] = self.matrix[self.size - j - 1][i]
                    self.matrix[self.size - j - 1][i] = self.matrix[self.size - 1 - i][self.size - j - 1]
                    self.matrix[self.size - 1 - i][self.size - j - 1] = self.matrix[j][self.size - i - 1]
                    self.matrix[j][self.size - i - 1] = aux
                else:
                    aux = self.matrix[i][j]
                    self.matrix[i][j] = self.matrix[j][self.size - i - 1]
                    self.matrix[j][self.size - i - 1] = self.matrix[self.size - 1 - i][self.size - j - 1]
                    self.matrix[self.size - 1 - i][self.size - j - 1] = self.matrix[self.size - j - 1][i]
                    self.matrix[self.size - j - 1][i] = aux

    def rotate(self):
        """
        Rotates the piece 90 degrees clockwise. The rotation is performed in-place.
        """
        self._rotate(clockwise=True)

    def unrotate(self):
        """
        Rotates the piece 90 degrees counterclockwise. The rotation is performed in-place.
        """
        self._rotate(clockwise=False)

    def _get_limits(self):
        """
        Calculates the iteration limits for rotating the matrix.

        Returns:
            tuple: Two integers representing the row and column iteration limits.
        """
        return self.size // 2, (self.size + 1) // 2

    def __getitem__(self, key):
        """
        Allows access to rows of the matrix using the subscript operator.

        Args:
            key (int): The row index to access.

        Returns:
            list: The row at the specified index.
        """
        return self.matrix[key]

    def get_color(self):
        """
        Retrieves the color of the piece.

        Returns:
            int: The color associated with the piece.
        """
        return self.color

    def __repr__(self):
        """
        Provides a string representation of the matrix for printing.

        Returns:
            str: A formatted string representing the matrix row by row.
        """
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])



   
PIECE_I = PieceForm(tetris_pieces['I'],2)
PIECE_O = PieceForm(tetris_pieces['O'],3)
PIECE_T = PieceForm(tetris_pieces['T'],4)
PIECE_L = PieceForm(tetris_pieces['L'],5)
PIECE_J = PieceForm(tetris_pieces['J'],6)
PIECE_S = PieceForm(tetris_pieces['S'],7)
PIECE_Z = PieceForm(tetris_pieces['Z'],8)










