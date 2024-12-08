import pygame
import copy
import numpy as np
import src.utils.pieceForm as pf
from src.constFile.constColors import tetris_colors
from src.constFile.constGame import CELL_SIZE

class Piece:
    """
    Represents a Tetris piece. Manages the position, rotation, and drawing of the piece on the screen.
    This class allows manipulating game pieces by moving, rotating, and adjusting them within a Tetris board.

    Attributes:
        x (int): The horizontal coordinate of the piece on the board.
        y (int): The vertical coordinate of the piece on the board.
        piece (pf.PieceForm): The shape of the piece (usually an object of the PieceForm class that defines the structure of the piece).
    """

    def __init__(self, x: int, y: int, block: pf.PieceForm = None) -> None:
        """
        Initializes a new piece with the given coordinates and optional shape.

        Args:
            x (int): The initial horizontal coordinate of the piece on the board.
            y (int): The initial vertical coordinate of the piece on the board.
            block (pf.PieceForm, optional): The shape of the piece. If not provided, assumed to be None.
        """
        self.x = x 
        self.y = y
        self.piece = copy.deepcopy(block)

    def get_height(self) -> int:
        """
        Returns the height of the piece.

        Returns:
            int: The height of the piece.
        """
        return self.y
    
    def get_width(self) -> int:
        """
        Returns the width of the piece.

        Returns:
            int: The width of the piece.
        """
        return self.x

    def rotate(self) -> None:
        """
        Rotates the piece 90 degrees clockwise.
        """
        self.piece.rotate()

    def unrotate(self) -> None:
        """
        Rotates the piece 90 degrees counterclockwise (undoes the rotation).
        """
        self.piece.unrotate()

    def move_right(self) -> None:
        """
        Moves the piece one cell to the right.
        """
        self.x += 1

    def move_left(self) -> None:
        """
        Moves the piece one cell to the left.
        """
        self.x -= 1

    def up(self) -> None:
        """
        Moves the piece one cell up.
        """
        self.y -= 1

    def down(self) -> None:
        """
        Moves the piece one cell down.
        """
        self.y += 1

    def set_position(self, x: int, y: int) -> None:
        """
        Sets the piece's position to the given coordinates.

        Args:
            x (int): The new horizontal coordinate of the piece.
            y (int): The new vertical coordinate of the piece.
        """
        self.x = x 
        self.y = y

    def centre_on(self, x: int, y: int) -> None:
        """
        Centers the piece on the given coordinates (adjusts its position
        so that its center matches the provided coordinates).

        Args:
            x (int): The horizontal coordinate to center the piece on.
            y (int): The vertical coordinate to center the piece on.
        """
        self.set_position(x - (self.size() - 1) // 2, y)

    def __getitem__(self, key: int) -> list:
        """
        Retrieves a row of the piece in its internal shape.

        Args:
            key (int): The row index to retrieve.

        Returns:
            list: A list representing the specified row of the piece.
        """
        return self.piece[key]
    
    def get_color(self) -> int:
        """
        Retrieves the color of the piece.

        Returns:
            int: The color of the piece.
        """
        return self.piece.get_color()
    
    def size(self) -> int:
        """
        Returns the size of the piece (i.e., the number of rows or columns).

        Returns:
            int: The size of the piece.
        """
        return self.piece.size
    
    def is_empty_row(self, row: int) -> bool:
        """
        Checks if a specific row of the piece is empty.

        Args:
            row (int): The row index to check.

        Raises:
            RuntimeError: If the row index is out of bounds for the piece.

        Returns:
            bool: True if the row is empty, False otherwise.
        """
        col = 0
        empty = True

        if row < self.size():
            while col < len(self.piece[row]) and empty:
                if self.piece[row][col] != 0:
                    empty = False
                col += 1
        else:
            raise RuntimeError("Row out of bounds")
        
        return empty
    
    def adjust_pos(self, sizex: int) -> None:
        """
        Adjusts the piece's position to ensure it stays within the horizontal bounds.

        Args:
            sizex (int): The maximum horizontal size of the board.
        """
        adjusted_posx = max(0, min(self.x, sizex - self.size()))
        self.set_position(adjusted_posx, self.y)

    def get_lines(self) -> list:
        """
        Retrieves the vertical lines (rows) that the piece occupies.

        Returns:
            list: A list of row indices that the piece occupies.
        """
        output = [i for i in range(self.y, self.y + self.size())]
        return output
    
    def draw(self, screen, pos) -> None:
        """
        Draws the piece on the given screen at the specified position.

        Args:
            screen: The pygame screen object to draw on.
            pos: A tuple (x, y) indicating the offset position where the piece will be drawn.
        """
        for i in range(self.size()):
            for j in range(self.size()):
                if self[i][j] == 1:
                    x = (self.x + j) * CELL_SIZE + pos[0]
                    y = (self.y + i) * CELL_SIZE + pos[1]
                    pygame.draw.rect(
                        screen,
                        tetris_colors[self.get_color()],
                        (x, y, CELL_SIZE, CELL_SIZE),
                        0
                    )
                    pygame.draw.rect(
                        screen,
                        (0, 0, 0),
                        (x, y, CELL_SIZE, CELL_SIZE),
                        1
                    )

    def into_numpy(self, grid: np.array):
        """
        Updates the given grid with the piece's shape, marking its cells.

        Args:
            grid (np.array): The game grid (2D numpy array) to update with the piece's shape.
        """
        for row in range(self.size()):
            for col in range(self.size()):
                if self[row][col] == 1:
                    grid[self.y + row][self.x + col] = 1

    def get_type(self) -> pf.PieceForm:
        """
        Returns the type (shape) of the piece.

        Returns:
            pf.PieceForm: The type of the piece.
        """
        return self.piece



