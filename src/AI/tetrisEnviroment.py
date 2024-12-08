import numpy as np
from collections import deque
from src.AI.preprocessing import Preprocessing
from src.game import Game  # Asegúrate de que la ruta sea correcta

class TetrisEnviroment:
    def __init__(self, tick_rate, set_pieces, grid_shape, num_next_pieces):
        self.grid_shape = grid_shape
        self.num_next_pieces = num_next_pieces
        self.tick_rate = tick_rate
        self.set_pieces = set_pieces
        self.game = Game(self.tick_rate, self.set_pieces)
        self.preprocessor = None

    def start_game():
        pass
        
    def calculate_reward():
        pass
    
    def get_max_height():
        pass

    def get_total_height():
        pass   

    def get_bumpiness():
        pass

