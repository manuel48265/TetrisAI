from src.board import Board
from src.shapeManager import ShapeManager
from collections import deque
from src.actions import Actions
from src.tetrisTimer import TetrisTimer
from src.player import Player
class Game: 
    def __init__(self, tick_rate: int, set_pieces : list, player : Player):

        self.board = None
        self.current_piece = None
        self.score = 0
        self.game_over = False
        self.manager = ShapeManager(len(set_pieces),set_pieces)
        self.next_pieces = deque()
        self.current_time = tick_rate
        self.timer = TetrisTimer(timeout_seconds=self.current_time,on_timeout_callback=self.move_piece_down())
        self.player = player
        
    def start(self, width : int, height : int, num_future_pieces: int):
        self.board = Board(width,height)
        self.next_pieces = self.manager.init_rand_deque(num_future_pieces)
        self.board.set_new_piece(self._get_new_piece())
        self.timer.start()

    def update(self):
        
        while(not self.game_over):
            action = self.player.next_action()
            if self.game_over:
                break
            self.handle_input(action)
        
    def increase_speed(self):
        self.timer.reduce_time()

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

    def finish_game(self):
        self.game_over = True
        self.timer.stop()
        return self.score

    def handle_input(self, act: Actions) -> None:
        if(not self.game_over):
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
        else: 
            self.finish_game()

    def print():
        pass
        

