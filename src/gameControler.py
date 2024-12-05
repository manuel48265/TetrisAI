from src.board import Board
from src.shapeManager import ShapeManager
from collections import deque
from src.actions import Actions
from src.tetrisTimer import TetrisTimer
from src.player import Player
from src.piece import Piece

class GameControler: 
    def __init__(self, tick_rate: float, set_pieces : list, player : Player):

        self.board = None
        self.score = 0
        self.level = 1
        self.running = True
        self.manager = ShapeManager(len(set_pieces),set_pieces)
        self.next_pieces = deque()
        self.current_time = tick_rate
        self.timer = TetrisTimer(time=self.current_time)
        self.player = player
        
    def start(self, width : int, height : int, num_future_pieces: int):
        self.board = Board(width,height)
        self.next_pieces = self.manager.init_rand_deque(num_future_pieces)
        print(self.board.set_new_piece(self._get_new_piece()))
        print(self.board.current_piece.x)
        self.timer.set_funct(self.move_piece_down)
        self.timer.start()

    def update(self,action):
        
        if(self.running):
            self.handle_input(action)

        return self.running

    def get_next_pieces(self):
        return self.next_pieces
    
    def get_board(self):
        return self.board

    def get_score(self):
        return self.score
    
    def get_level(self):
        return self.level
    
    def get_game_state(self):
        return self.running
    
    def increase_speed(self):
        self.timer.reduce_time()

    def _get_new_piece(self) -> Piece:
        print(self.next_pieces)
        self.next_pieces.append(self.manager.get_random_piece())
        return self.next_pieces.popleft()
    
    def move_piece_down(self):

        if(not self.board.move_piece_down()):
            self.score += self.board.update_and_return_points()
            if(not self.board.set_new_piece(self._get_new_piece())):
                self.finish_game()

        self.timer.reset()

    def _timer_condition(self,func):
        if(func()):
            self.timer.reset()

    def finish_game(self):
        self.running = False
        self.timer.stop()
        print("Has Perdido")

    def handle_input(self, act: Actions) -> None:
        if(self.running):
            match act: 
                case Actions.ROTATE:
                    self._timer_condition(self.board.rotate_piece)
                case Actions.RIGHT:
                    self._timer_condition(self.board.move_piece_rigth)
                case Actions.LEFT:
                    self._timer_condition(self.board.move_piece_left)
                case Actions.DOWN:
                    self.move_piece_down()
                case _:
                    pass

    def print():
        pass
        

