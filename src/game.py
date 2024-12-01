from src.board import Board
from src.shapeManager import ShapeManager
from collections import deque
from src.actions import Actions
from src.tetrisTimer import Timer
class Game: 
    def __init__(self, tick_rate: int, set_pieces : list):

        self.board = None
        self.current_piece = None
        self.score = 0
        self.game_over = False
        self.manager = ShapeManager(len(set_pieces),set_pieces)
        self.next_pieces = deque()
        self.timer = Timer(timeout_seconds=tick_rate,on_timeout_callback=self.move_piece_down())
        
    def start(self, width : int, height : int, num_future_pieces: int):
        self.board = Board(width,height)
        self.next_pieces = self.manager.init_rand_deque(num_future_pieces)
        self.board.set_new_piece(self._get_new_piece())
        self.timer.start()

    def update():
        #print board, pieces and more
        pass

    def _get_new_piece(self):
        self.next_pieces.append(self.manager.get_random_piece())
        return self.next_pieces.pop()
    
    def move_piece_down(self):

        if(not self.board.move_piece_down()):
            self.points += self.board.update_and_return_points()
            self._get_new_piece()

        self.timer.reset()

    def _timer_condition(self,func):
        if(func()):
            self.timer.reset()

    def game_over(self):
        self.timer.stop()
        #Finish the game.
        
        pass 

    def handle_input(self, act: Actions) -> None:
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
        

