import time
from src.board import Board
from src.utils.shapeManager import ShapeManager
from collections import deque
from src.utils.actions import Actions
from src.utils.tetrisTimer import TetrisTimer
from src.piece import Piece

class Game:
    """
    A class to manage the Tetris game logic, including the game board, pieces, scoring, and handling user inputs.

    Attributes:
        board (Board): The game board where pieces are placed and manipulated.
        score (int): The current score of the player.
        level (int): The current game level, which increases as the score progresses.
        running (bool): A flag indicating whether the game is running or has ended.
        manager (ShapeManager): The shape manager responsible for generating Tetris pieces.
        next_pieces (deque): A queue holding the next set of Tetris pieces.
        current_time (float): The time interval between automatic piece drops.
        timer (TetrisTimer): A timer responsible for automatically moving the piece down after a certain interval.

    Methods:
        start(width: int, height: int, num_future_pieces: int):
            Initializes the game, including setting up the board and generating the initial pieces.

        get_num_pieces() -> int:
            Returns the number of available piece types.

        update(action: Actions) -> bool:
            Updates the game based on the player's action and returns whether the game is still running.

        get_next_pieces() -> deque:
            Returns the queue of upcoming pieces.

        get_board() -> Board:
            Returns the current game board.

        get_score() -> int:
            Returns the current score.

        get_level() -> int:
            Returns the current level.

        get_game_state() -> bool:
            Returns the game state (True if the game is running, False if it has finished).

        increase_speed():
            Increases the speed at which pieces drop.

        _get_new_piece() -> Piece:
            Generates a new piece from the shape manager and adds it to the game board.

        move_piece_down():
            Moves the current piece down, checks for collision, updates the score, and generates a new piece.

        finish_game():
            Ends the game and stops the timer.

        handle_input(act: Actions) -> None:
            Handles user input to control the movement and rotation of the current piece.
    """

    def __init__(self, tick_rate: float, set_pieces: list):
        """
        Initializes the Game object.

        Args:
            tick_rate (float): The time interval between automatic piece drops.
            set_pieces (list): A list of available Tetris pieces.
        """
        self.board = None
        self.score = 0
        self.level = 1
        self.running = True
        self.manager = ShapeManager(len(set_pieces), set_pieces)
        self.next_pieces = deque()
        self.current_time = tick_rate
        self.timer = TetrisTimer(time=self.current_time)
        self.future_pieces = None
        
    def start(self, width: int, height: int, num_future_pieces: int):
        """
        Starts the game, initializes the board, and generates the first set of pieces.

        Args:
            width (int): The width of the game board.
            height (int): The height of the game board.
            num_future_pieces (int): The number of upcoming pieces to pre-generate.
        """
        self.board = Board(width, height)
        self.future_pieces = num_future_pieces
        self.next_pieces = self.manager.init_rand_deque(num_future_pieces)
        self.board.set_new_piece(self._get_new_piece())
        self.timer.set_funct(self.move_piece_down)
        self.timer.start()

    def reset(self,time=None):
        """
        Resets the game to its initial state.
        """
        self.board.reset()
        self.score = 0
        self.level = 1
        self.running = True
        self.next_pieces.clear()
        if time is not None:
            self.current_time = time
        self.timer = TetrisTimer(time=self.current_time)
        self.next_pieces = self.manager.init_rand_deque(self.future_pieces)
        self.board.set_new_piece(self._get_new_piece())
        self.timer.set_funct(self.move_piece_down)
        self.timer.start()
       

    def get_num_pieces(self):
        """
        Returns the number of available piece types.

        Returns:
            int: The number of available piece types.
        """
        return self.manager.get_num_pieces()
    
    def is_game_over(self):
        """
        Returns whether the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return not self.running

    def update(self, action):
        """
        Updates the game state based on the player's input action.

        Args:
            action (Actions): The action performed by the player (rotate, move left, move right, etc.).

        Returns:
            bool: Whether the game is still running.
        """
        if self.running:
            self.handle_input(action)
        return self.running

    def get_next_pieces(self):
        """
        Returns the queue of upcoming pieces.

        Returns:
            deque: The next set of pieces to be used.
        """
        return self.next_pieces
    
    def get_board(self) -> Board:
        """
        Returns the current game board.

        Returns:
            Board: The current game board.
        """
        return self.board

    def get_score(self):
        """
        Returns the current score.

        Returns:
            int: The current score.
        """
        return self.score
    
    def get_level(self):
        """
        Returns the current level.

        Returns:
            int: The current level.
        """
        return self.level
    
    def get_game_state(self):
        """
        Returns the current game state.

        Returns:
            bool: True if the game is running, False if it has finished.
        """
        return self.running
    
    def increase_speed(self):
        """
        Increases the speed at which pieces drop.
        """
        self.timer.reduce_time()

    def _get_new_piece(self) -> Piece:
        """
        Generates a new piece and adds it to the game.

        Returns:
            Piece: The new piece to be placed on the board.
        """
        self.next_pieces.append(self.manager.get_random_piece())
        return self.next_pieces.popleft()
    
    def move_piece_down(self):
        """
        Moves the current piece down. If it collides with the bottom or other pieces, the piece is set
        and a new piece is generated. The score is updated based on cleared lines.

        If a new piece cannot be placed, the game ends.
        """
        if not self.board.move_piece_down():
            self.score += self.board.update_and_return_points()
            if not self.board.set_new_piece(self._get_new_piece()):
                self.finish_game()
        self.timer.reset()

    def finish_game(self):
        """
        Ends the game and stops the timer.
        """
        self.running = False
        self.timer.stop()


    def handle_input(self, act: Actions) -> None:
        """
        Handles the player's input to move or rotate the current piece.

        Args:
            act (Actions): The action to perform (rotate, move left, move right, move down).
        """
        if self.running:
            match act: 
                case Actions.ROTATE:
                    self.board.rotate_piece()
                case Actions.RIGHT:
                    self.board.move_piece_right()
                case Actions.LEFT:
                    self.board.move_piece_left()
                case Actions.DOWN:
                    self.move_piece_down()
                    #self.score += 1
                case _:
                    pass
    
    def get_current_piece(self) -> Piece:
        """
        Returns the current piece on the board.

        Returns:
            Piece: The current piece on the board.
        """
        return self.board.get_current_piece()  
        

