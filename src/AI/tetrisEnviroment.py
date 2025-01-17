import numpy as np
import random
from collections import deque
from src.utils.actions  import Actions
from src.AI.preprocessing import Preprocessing
from src.game import Game  

class TetrisEnviroment:

    HOLES_WEIGHT = -(0.8)
    MAX_HEIGHT_WEIGHT = -(0)
    AVG_HEIGHT_WEIGHT = -(0.05)
    HEIGHT_DIFF_WEIGHT = -(0.18)
    POINTS_WEIGHT = 0.02

    def __init__(self, tick_rate, set_pieces, grid_shape, num_next_pieces) -> None:
        self.grid_shape = grid_shape
        self.num_next_pieces = num_next_pieces
        self.tick_rate = tick_rate
        self.set_pieces = set_pieces
        self.game = Game(self.tick_rate, self.set_pieces)
        self.preprocessor = None
        self.parents_map = None
        self.final_states = None
        self.temporal_memory = None

    def start(self) -> None:
        self.game.start(self.grid_shape[0], self.grid_shape[1], self.num_next_pieces)
        self.preprocessor = Preprocessing(self.game.get_board().get_grid(), self.game.get_current_piece(), self.game.get_next_pieces(), self.set_pieces, max_num_pieces=self.num_next_pieces)

    def reset(self) -> None:
        self.game.reset()
        self.preprocessor = Preprocessing(self.game.get_board().get_grid(), self.game.get_current_piece(), self.game.get_next_pieces(), self.set_pieces, max_num_pieces=self.num_next_pieces)
        
    def calculate_reward(self, metrics) -> float:

        reward = 100

        reward += self.HOLES_WEIGHT * metrics["holes"] 
        reward += self.MAX_HEIGHT_WEIGHT * metrics["max_height"]
        reward += self.AVG_HEIGHT_WEIGHT * metrics["avg_height"] 
        reward += self.HEIGHT_DIFF_WEIGHT * metrics["height_diff"] 
        reward += self.POINTS_WEIGHT * metrics["points"]

        if not metrics['done']: 
            reward = -100

        return reward
    
    def calc_states(self):
        self.final_states, self.parents_map = self.game.get_board().valid_future_positions_with_parents()

    def get_path(self,final_pos):
        return self.game.get_board().get_path(final_pos, self.parents_map)
    
    def calculate_reward_model(self, model : list, input_vals : np.array) -> np.array:

        for i in range(len(model)-1):
            input_vals = np.maximum(0,input_vals@model[i])
            input_vals = np.append(input_vals,self.preprocessor.transform_piece(self.game.get_next_pieces()[i+1]))
            input_vals = np.append(input_vals,np.ones(1))

        val = input_vals@model[-1]
        return val

    def get_max_heuristic_model(self, model : list):
        self.calc_states()
        max = -10000
        max_state = self.final_states[0]
        holes = 100
        avg_height = 18

        for state in self.final_states:
            metrics = self.game.get_board().get_metrics_pos(state,self.game.next_pieces[0])
            #reward = self.calculate_reward(metrics)
            if metrics['done']:
                input_vals = np.array([])
                for i in range(self.grid_shape[0]):
                    input_vals = np.append(input_vals,metrics['col ' + str(i)])

                input_vals = np.append(input_vals,metrics['holes'])
                input_vals = np.append(input_vals,metrics['height_diff'])
                input_vals = np.append(input_vals,metrics['avg_height'])

                input_vals = np.append(input_vals,self.preprocessor.transform_piece(self.game.get_next_pieces()[0]))
                input_vals = np.append(input_vals,np.ones(1))

                reward = self.calculate_reward_model(model,input_vals).item()

                if reward > max:
                    max = reward
                    max_state = state
                    holes = metrics['holes']
                    avg_height = metrics['avg_height']

        return max_state, holes, avg_height
    
    def get_max_heuristic_model_simple(self, model : list):
        self.calc_states()
        max = -10000
        max_state = self.final_states[0]

        for state in self.final_states:
            metrics = self.game.get_board().get_metrics_pos(state,self.game.next_pieces[0])
            #reward = self.calculate_reward(metrics)
            if metrics['done']:
                input_vals = np.array([])
                for i in range(self.grid_shape[0]):
                    input_vals = np.append(input_vals,metrics['col ' + str(i)])

                input_vals = np.append(input_vals,metrics['holes'])
                input_vals = np.append(input_vals,metrics['height_diff'])
                input_vals = np.append(input_vals,metrics['avg_height'])

                input_vals = np.append(input_vals,self.preprocessor.transform_piece(self.game.get_next_pieces()[0]))
                input_vals = np.append(input_vals,np.ones(1))

                reward = self.calculate_reward_model(model,input_vals).item()

                if reward > max:
                    max = reward
                    max_state = state

        return max_state
    

    def get_max_heuristic(self):
        self.calc_states()
        max = -10000
        max_state = None

        for state in self.final_states:
            metrics = self.game.get_board().get_metrics_pos(state,self.game.next_pieces[0])
            reward = self.calculate_reward(metrics)

            if reward > max:
                max = reward
                max_state = state

        return max_state

    def step(self,final_pos) -> tuple:

        self.calc_states()

        self.temporal_memory = []

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
    
    
    


