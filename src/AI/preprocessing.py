import numpy as np 
from collections import deque
from typing import Deque
from src.piece import Piece
from src.utils import pieceForm as pf

class Preprocessing:
    def __init__(self, grid: list, piece : Piece, next_pieces : deque, piece_set : list, max_num_pieces = 3):
        self.num_pieces = len(piece_set)
        # We save our pieces as a reversed map to improve the performance iterating over the pieces.
        self.piece_set= {element: i for i, element in enumerate(piece_set)}
        self.max_num_pieces = max_num_pieces - 1
        self.grid = self.transform_grid(grid)
        self.piece = self.transform_piece(piece)
        self.next_pieces = self.transform_next_pieces(next_pieces)
        
    def transform_grid(self,grid):
        output = np.zeros((len(grid),len(grid[0])))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] != 0:
                    output[i][j] = 1
        
        return output
    def transform_piece(self,piece : Piece) -> np.array:
        output = np.zeros(self.num_pieces)
        piece_type = piece.get_type()
        if piece_type not in self.piece_set:
            raise KeyError(f"Tipo de pieza no encontrado en piece_set: {piece_type}")
        output[self.piece_set[piece_type]] = 1
        return output
    
    def transform_next_pieces(self,next_pieces: Deque[Piece]):
        one_hot_piezas = np.zeros((min(len(next_pieces),self.max_num_pieces), self.num_pieces))
        for i in range(min(len(next_pieces),self.max_num_pieces)):
            piece = next_pieces[i]
            piece_type = piece.get_type()
            if piece_type not in self.piece_set:
                raise KeyError(f"Tipo de pieza no encontrado en piece_set: {piece_type}")
            one_hot_piezas[i, self.piece_set[piece_type]] = 1
        return one_hot_piezas.flatten()  # Combinar en un solo vector

    def update(self,piece:Piece, grid: list, next_pieces: deque):
        self.next_pieces = self.transform_next_pieces(next_pieces)
        self.grid = self.transform_grid(grid)
        self.piece = self.transform_piece(piece)

    def get_input(self):
        
        hot_vector = np.copy(self.piece)
        hot_vector = np.concatenate((hot_vector, self.next_pieces))
        grid_3d = np.expand_dims(self.grid, axis=-1)
        #add batch dimension
        grid_3d = np.expand_dims(grid_3d, axis=0) 
        hot_vector = np.expand_dims(hot_vector, axis=0)
        grid_3d_y = grid_3d.copy()

        output ={
            "input_x": grid_3d,
            "input_y": grid_3d_y,
            "input_vector": hot_vector
        }

        return output
    
    def get_input_size(self):
        return self.combine_grid_and_piece().shape, self.next_pieces.shape
    
    


    



