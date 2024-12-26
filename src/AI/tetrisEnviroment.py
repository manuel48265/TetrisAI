import numpy as np
import random
from collections import deque
from src.utils.actions  import Actions
from src.AI.preprocessing import Preprocessing
from src.game import Game  

class TetrisEnviroment:

    HOLES_WEIGHT = -(0.35)
    MAX_HEIGHT_WEIGHT = -(0.1)
    AVG_HEIGHT_WEIGHT = -(0.05)
    HEIGHT_DIFF_WEIGHT = -(0.18)
    POINTS_WEIGHT = 0.01

    def __init__(self, tick_rate, set_pieces, grid_shape, num_next_pieces) -> None:
        self.grid_shape = grid_shape
        self.num_next_pieces = num_next_pieces
        self.tick_rate = tick_rate
        self.set_pieces = set_pieces
        self.game = Game(self.tick_rate, self.set_pieces)
        self.preprocessor = None
        self.parents_map = None
        self.final_states = None

    def start(self) -> None:
        self.game.start(self.grid_shape[0], self.grid_shape[1], self.num_next_pieces)
        self.score = self.game.get_score()
        self.preprocessor = Preprocessing(self.game.get_board().get_grid(), self.game.get_current_piece(), self.game.get_next_pieces(), self.set_pieces, max_num_pieces=self.num_next_pieces)

    def reset(self) -> None:
        self.game.reset()
        self.score = self.game.get_score()
        self.preprocessor = Preprocessing(self.game.get_board().get_grid(), self.game.get_current_piece(), self.game.get_next_pieces(), self.set_pieces)
        
    def calculate_reward(self, metrics) -> float:

        reward = 10

        reward += self.HOLES_WEIGHT * metrics["holes"] 
        reward += self.MAX_HEIGHT_WEIGHT * metrics["max_height"] 
        reward += self.AVG_HEIGHT_WEIGHT * metrics["avg_height"] 
        reward += self.HEIGHT_DIFF_WEIGHT * metrics["height_diff"] 
        reward += self.POINTS_WEIGHT * metrics["points"]

        return reward
    
    def calc_states(self):
        self.final_states, self.parents_map = self.game.get_board().valid_future_positions_with_parents()
    
        
    def model_state(self,model):
        max = -100000
        final_pos = None
        for state in self.final_states:
            grid = self.game.get_board().evaluate_final_pos(state)
            next_pieces = []
            for i in range(len(self.game.next_pieces)-1):
                next_pieces.append(self.game.next_pieces[i+1])

            self.preprocessor.update(self.game.next_pieces[0],grid, next_pieces)
            input = self.preprocessor.get_input()
            model.predict(input)
            if max < model.predict(input):
                max = model.predict(input)
                final_pos = state

        return final_pos

    def step(self,final_pos) -> tuple:

        self.calc_states()

        path = self.game.get_board().get_path(final_pos,self.parents_map)
        reward = self.calculate_reward(final_pos)

        for action in path:
            self.game.update(action)
        
        done = self.game.is_game_over()
        if done:
            reward -= 100

        self.preprocessor.update(self.game.get_current_piece(),self.game.get_board().get_grid(), self.game.get_next_pieces())

        return self.preprocessor.get_input(), reward, done
    
    def get_state(self) -> np.ndarray:
        return self.preprocessor.get_input()
    
    


