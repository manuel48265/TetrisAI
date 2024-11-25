from constPieces import tetris_pieces
class PieceForm:
    def __init__(self,matrix,color) -> None:
        """
        Initializes the piece with a matrix representing its shape.
        
        Args:
            matrix (list of list of int): A 2D matrix representing the shape of the piece.
        """
        self.matrix = matrix  # The matrix representing the shape of the piece.
        self.size = len(matrix)  # The size of the matrix (its dimension, assuming it's square).
        self.color = color

    def rotate(self):
        """
        Rotates the piece 90 degrees clockwise. The rotation is done in-place on the piece's matrix.

        The rotation is performed by swapping values in the 2D matrix.
        This involves moving values in corresponding positions cyclically.
        """
        i_limit = self.size // 2  # Limit for the rows (half of the matrix).
        j_limit = 0  # Initialize the limit for the columns.

        # Adjust the column limit based on whether the size is even or odd.
        if self.size % 2 == 0:
            j_limit = self.size // 2  # If the size is even, take the exact half.
        else:
            j_limit = self.size // 2 + 1  # If the size is odd, the limit is slightly larger.

        # Iterate over the positions of the matrix and rotate the values in the opposite positions.
        for i in range(i_limit):
            for j in range(j_limit):
                # Perform a cycle of swaps between corresponding positions in the matrix.
                aux = self.matrix[i][j]
                self.matrix[i][j] = self.matrix[self.size - j - 1][i]
                self.matrix[self.size - j - 1][i] = self.matrix[self.size - 1 - i][self.size - j - 1]
                self.matrix[self.size - 1 - i][self.size - j - 1] = self.matrix[j][self.size - i - 1]
                self.matrix[j][self.size - i - 1] = aux

    def unrotate(self):
        """
        Undo a 90-degree clockwise rotation (equivalent to rotating counterclockwise).

        The logic is the inverse of the rotation: values move cyclically in a counterclockwise direction.
        """
        i_limit = self.size // 2  # Limit for the rows.
        j_limit = 0  # Initialize the limit for the columns.

        # Adjust the column limit depending on whether the size is even or odd.
        if self.size % 2 == 0:
            j_limit = self.size // 2  # If the size is even, the column limit is half.
        else:
            j_limit = self.size // 2 + 1  # If the size is odd, the column limit is slightly larger.

        # Iterate over the positions of the matrix and move the values in reverse rotation.
        for i in range(i_limit):
            for j in range(j_limit):
                # Perform a reverse cycle of swaps between corresponding positions in the matrix.
                aux = self.matrix[i][j]
                self.matrix[i][j] = self.matrix[j][self.size - i - 1]
                self.matrix[j][self.size - i - 1] = self.matrix[self.size - 1 - i][self.size - j - 1]
                self.matrix[self.size - 1 - i][self.size - j - 1] = self.matrix[self.size - j - 1][i]
                self.matrix[self.size - j - 1][i] = aux

    def __getitem__(self, key):
        return self.matrix[key]
    def get_color(self):
        return self.color
    def __repr__(self):
        """
        Provides a string representation of the matrix for printing.
        
        Returns:
            str: A formatted string that represents the matrix row by row.
        """
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])


   
PIECE_I = PieceForm(tetris_pieces['I'],2)
PIECE_O = PieceForm(tetris_pieces['O'],3)
PIECE_T = PieceForm(tetris_pieces['T'],4)
PIECE_L = PieceForm(tetris_pieces['L'],5)
PIECE_J = PieceForm(tetris_pieces['J'],6)
PIECE_S = PieceForm(tetris_pieces['S'],7)
PIECE_Z = PieceForm(tetris_pieces['Z'],8)



for i in range(5):
    print(PIECE_O.size,"\n")
    print(PIECE_O)
    PIECE_O.rotate()
    print("\n")










