import pygame
import copy
from collections import deque
from src.piece import Piece
import src.utils.pieceForm as pf
from src.constFile.constGame import CELL_SIZE, EMPTY_CELL
from src.constFile.constColors import tetris_colors
from src.utils.actions import Actions

class Board:
    """
    Represents the Tetris game board, including methods for managing
    pieces, validating their positions, and updating the grid state.
    
    Attributes:
        width (int): The width of the board (number of columns).
        height (int): The height of the board (number of rows).
        grid (list): A 2D list representing the board, where each cell
                     holds a color code for a piece (0 if empty).
        current_piece (Piece): The currently active Tetris piece.
        points (dict): A dictionary mapping the number of cleared lines
                       to the corresponding point value.
    """
    def __init__(self, width: int, height: int) -> None:
        """
        Initializes the game board with the given width and height.

        Args:
            width (int): The number of columns in the board.
            height (int): The number of rows in the board.
        """
        self.width = width
        self.height = height
        self.grid = [[EMPTY_CELL for _ in range(width)] for _ in range(height)]
        self.current_piece = None
        self.points = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}

    def reset(self) -> None:
        """
        Resets the game board to its initial state.
        """
        self.grid = [[EMPTY_CELL for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = None
    
    def is_valid_position(self) -> bool:
        """
        Checks if the current piece is in a valid position on the board.
        Validates the piece's position by ensuring it does not overlap 
        with other pieces or extend outside the board boundaries.

        Returns:
            bool: True if the piece is in a valid position, False otherwise.
        """
        for i in range(self.current_piece.size()):
            for j in range(self.current_piece.size()):
                if self.current_piece[i][j] == 1:
                    posx = self.current_piece.x + j
                    posy = self.current_piece.y + i
                    bad_x = posx >= self.width or posx < 0
                    bad_y = posy < 0 or posy >= self.height
                    if bad_x or bad_y or self.grid[posy][posx] != EMPTY_CELL:
                        return False
        return True
    
    def get_grid(self) -> list:
        """
        Returns the current state of the game board.

        Returns:
            list: A 2D list representing the game board.
        """
        return self.grid

    def _cols_down(self, lines: list) -> None:
        """
        Moves the rows above the cleared lines down by one.

        Args:
            lines (list): A list of line indices that have been cleared.
        """

        current_line = next_line = self.height - 1
        while next_line >= 0:
            while next_line in lines:
                next_line -= 1

            if next_line >= 0:
                self.grid[current_line] = self.grid[next_line]

            current_line -= 1
            next_line -= 1

        for i in range(len(lines)):
            self.grid[i] = [0] * self.width

    def set_new_piece(self, piece: Piece) -> bool:
        """
        Sets a new piece on the board and checks if it fits in the 
        specified position. If the piece cannot be placed, returns False.

        Args:
            piece (Piece): The piece to be placed on the board.

        Returns:
            bool: True if the piece was placed successfully, False if the 
                  game is over or placement is invalid.
        """
        self.current_piece = piece
        new_x = (self.width - 1) // 2
        new_y = 0
        self.current_piece.centre_on(new_x, new_y)

        if self.is_valid_position():
            return True

        # Try placing piece by shifting down if necessary
        for i in range(self.height):
            if self.current_piece.is_empty_row(i):
                self.current_piece.centre_on(new_x, -i-1)
                if self.is_valid_position():
                    return True
            else:
                return False
            
        return False
    def rotate_piece(self) -> bool:
        """
        Rotates the current piece clockwise and checks if the new 
        position is valid. If the rotation is invalid, it reverts the 
        piece back to its original position.

        Returns:
            bool: True if the piece was successfully rotated, False otherwise.
        """

        output = True

        pos_x, pos_y = self.current_piece.x, self.current_piece.y
        self.current_piece.adjust_pos(self.width)
        self.current_piece.rotate()

        if not self.is_valid_position():
            output = False
            self.current_piece.unrotate()
            self.current_piece.set_position(pos_x, pos_y)
        
        return output

    def move_piece_down(self) -> bool:
        """
        Moves the current piece down by one row. If the piece cannot move
        down due to collision or reaching the bottom of the board, it is locked.

        Returns:
            bool: True if the piece was successfully moved, False otherwise.
        """

        if self.can_move_piece_down():
            return True
        else:
            self.lock_piece()
            return False
        
    
    def can_move_piece_down(self) -> bool:

        output = True
        self.current_piece.down()

        if not self.is_valid_position():
            self.current_piece.up()
            output = False
        
        return output


    def move_piece_right(self) -> bool:
        """
        Moves the current piece to the right by one column. If the piece 
        cannot move right due to collision or boundaries, it reverts.

        Returns:
            bool: True if the piece was successfully moved, False otherwise.
        """
        output = True
        self.current_piece.move_right()

        if not self.is_valid_position():
            self.current_piece.move_left()
            output = False

        return output

    def move_piece_left(self) -> bool:
        """
        Moves the current piece to the left by one column. If the piece 
        cannot move left due to collision or boundaries, it reverts.

        Returns:
            bool: True if the piece was successfully moved, False otherwise.
        """
        output = True
        self.current_piece.move_left()

        if not self.is_valid_position():
            self.current_piece.move_right()
            output = False

        return output

    def lock_piece(self) -> None:
        """
        Locks the current piece in place on the board by updating the grid 
        with the piece's color.
        """
        for i in range(self.current_piece.size()):
            for j in range(self.current_piece.size()):
                if self.current_piece[i][j] == 1:
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.get_color()

    def update_and_return_points(self) -> int:
        """
        Updates the board after a piece has been locked and returns the points 
        for any cleared lines.

        Returns:
            int: The number of points earned from clearing lines.
        """
        lines = self.current_piece.get_lines()
        lines = self.identify_lines(lines)
        if len(lines) != 0:
            self._cols_down(lines)
        return self._get_points_for_clear_lines(len(lines))

    def identify_lines(self, lines: list) -> list:
        """
        Identifies the lines that are completely filled and need to be cleared.

        Args:
            lines (list): A list of line indices to check.

        Returns:
            list: A list of indices of lines that are completely filled.
        """
        total = []
        for line in lines:
            if line < self.height and sum(1 for i in range(self.width) if self.grid[line][i] != EMPTY_CELL) == self.width:
                total.append(line)
        
        return total


    def _get_points_for_clear_lines(self, num_lines) -> int:
        """
        Returns the points corresponding to the number of cleared lines.

        Args:
            num_lines (int): The number of cleared lines.

        Returns:
            int: The number of points awarded for clearing lines.
        """
        return self.points[num_lines]

    def get_current_piece(self) -> Piece:
        """
        Returns the current active piece on the board.

        Returns:
            Piece: The current piece on the board.
        """
        return self.current_piece
    
    def get_metrics(self) -> dict:
        """
        Returns the metrics of the board.

        Returns:
            dict: A dictionary containing the metrics of the board.
        """
    
        metrics = {
            'holes': 0.0,
            'max_height': 0.0,
            'avg_height': 0.0,
            'height_diff': 0.0,
            'points': 0.0
        }

        heights = [0] * self.width
        max_height = 0
        holes = 0
        height_diff = 0
        total_height = 0

        for col in range(self.width):
            empty = True
            for row in range(self.height):
                if self.grid[row][col] != EMPTY_CELL:
                    if empty:
                        empty = False
                        max_height= max(max_height, self.height - row)
                        heights[col] = self.height - row

                elif not empty:
                    holes += 1
                    
        for i in range(self.width):
            total_height += heights[i]
        
        for i in range(len(heights) - 1):
            height_diff += abs(heights[i] - heights[i + 1])
            
        for i in range(len(heights)):
            metrics['col ' + str(i)] = heights[i]/self.height

        metrics['height_diff'] = height_diff
        metrics['holes'] = holes
        metrics['max_height'] = max_height
        metrics['avg_height'] = total_height/self.width
        
        return metrics

    def valid_future_positions_with_parents(self):
        original_piece = copy.deepcopy(self.current_piece)

        visited = set()  # Set para almacenar estados únicos
        parent_map = {}  # Mapa para rastrear el padre de cada estado
        start_row = self.current_piece.y
        start_col = self.current_piece.x
        states = deque([(0, start_row, start_col)])  # (rotación_index, fila, columna)
        final_states = []
        visited.add((0, start_row, start_col))

        while states:
            state = states.popleft()
            rotation, row, col = state
            self.current_piece = copy.deepcopy(original_piece)
            for i in range(rotation):
                self.current_piece.rotate()
            self.current_piece.set_position(col, row)

            # Intentar mover a la izquierda
            if self.move_piece_left():
                new_state = (rotation, self.current_piece.y, self.current_piece.x)
                if new_state not in visited:
                    states.append(new_state)
                    visited.add(new_state)
                    parent_map[new_state] = state  # Registrar el padre
                self.current_piece.move_right()
            
            # Intentar mover a la derecha
            if self.move_piece_right():
                new_state = (rotation, self.current_piece.y, self.current_piece.x)
                if new_state not in visited:
                    states.append(new_state)
                    visited.add(new_state)
                    parent_map[new_state] = state  # Registrar el padre
                self.current_piece.move_left()

            # Intentar rotar
            if self.rotate_piece():
                new_state = ((rotation + 1) % 4, self.current_piece.y, self.current_piece.x)
                if new_state not in visited:
                    states.append(new_state)
                    visited.add(new_state)
                    parent_map[new_state] = state  # Registrar el padre
                self.current_piece.unrotate()
                self.current_piece.set_position(col,row)

            # Intentar mover hacia abajo
            if self.can_move_piece_down():
                new_state = (rotation, self.current_piece.y, self.current_piece.x)
                if new_state not in visited:
                    states.append(new_state)
                    visited.add(new_state)
                    parent_map[new_state] = state  # Registrar el padre
            else:
                final_states.append((rotation, row, col))

        self.current_piece = copy.deepcopy(original_piece)

        return final_states, parent_map
    
    def get_path(self,final_pos, parent_map):
        path = []
        path.append(Actions.DOWN)
        current = final_pos
        while current in parent_map:
            path.append(self.get_action_from_positions(parent_map[current], current))
            current = parent_map[current]

        path.reverse()
        return path

    def get_action_from_positions(self,parent_pos, current_pos):
        """
        Given a parent position and a current position, returns the action needed to reach the current position from the parent position.

        Args:
            parent_pos (tuple): The parent position (rotation, row, col).
            current_pos (tuple): The current position (rotation, row, col).

        Returns:
            str: The action needed to reach the current position from the parent position.
        """
        parent_rotation, parent_row, parent_col = parent_pos
        current_rotation, current_row, current_col = current_pos

        if parent_rotation != current_rotation:
            return Actions.ROTATE
        elif parent_col < current_col:
            return Actions.RIGHT
        elif parent_col > current_col:
            return Actions.LEFT
        elif parent_row < current_row:
            return Actions.DOWN
        else:
            return Actions.IDLE

    def evaluate_final_pos(self,final_pos):
        
        original_piece = copy.deepcopy(self.current_piece)
        original_grid = copy.deepcopy(self.grid)

        for i in range(final_pos[0]):
            self.current_piece.rotate()
        self.current_piece.set_position(final_pos[2], final_pos[1])


        self.lock_piece()
        #points = self.update_and_return_points()
        #metrics = self.get_metrics()

        #metrics['points'] = points

        grid = copy.deepcopy(self.grid)

        self.current_piece = original_piece
        self.grid = original_grid

        return grid
    
    def get_metrics_pos(self,final_pos, next_piece):

        original_piece = copy.deepcopy(self.current_piece)
        original_grid = copy.deepcopy(self.grid)
        next_piece = copy.deepcopy(next_piece)

        for i in range(final_pos[0]):
            self.current_piece.rotate()
        self.current_piece.set_position(final_pos[2], final_pos[1])

        self.lock_piece()
        points = self.update_and_return_points()
        metrics = self.get_metrics()

        metrics['points'] = points
        
        metrics['done'] = self.set_new_piece(next_piece)

        self.current_piece = original_piece
        self.grid = original_grid

        return metrics
    
    
    def draw(self, screen, pos) -> None:
        """
        Draws the current state of the board and the pieces on the screen.

        Args:
            screen (pygame.Surface): The screen where the board will be drawn.
            pos (tuple): The (x, y) position on the screen where the board will be drawn.
        """
        for row in range(self.height):
            for col in range(self.width):
                x = col * CELL_SIZE + pos[0]
                y = row * CELL_SIZE + pos[1]
                draw_border = 0
                if self.grid[row][col] == 0:
                    draw_border = 1
                pygame.draw.rect(screen, tetris_colors[self.grid[row][col]], (x, y, CELL_SIZE, CELL_SIZE), width=draw_border)



