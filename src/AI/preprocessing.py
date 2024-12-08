import numpy as np 
from collections import deque
from typing import Deque
from src.piece import Piece

from src.utils import pieceForm as pf

class Preprocessing:
    def __init__(self, grid: list, piece : Piece, next_pieces : deque, piece_set : list):
        self.num_pieces = len(piece_set)
        # We save our pieces as a reversed map to improve the performance iterating over the pieces.
        self.piece_set= {element: i for i, element in enumerate(piece_set)}
        self.grid = np.array(grid)
        self.piece = self.transform_piece(piece,self.grid.shape[0],self.grid.shape[1])
        self.next_pieces = self.transform_next_pieces(next_pieces)

    def transform_piece(self,piece : Piece, heigth : int, width : int):
        output = np.zeros((heigth,width))
        piece.into_numpy(output)
        return output
    
    def transform_next_pieces(self,next_pieces: Deque[Piece]):
        one_hot_piezas = np.zeros((len(next_pieces), self.num_pieces))
        for i, piece in enumerate(next_pieces):
            piece_type = piece.get_type()
            if piece_type not in self.piece_set:
                raise KeyError(f"Tipo de pieza no encontrado en piece_set: {piece_type}")
            one_hot_piezas[i, self.piece_set[piece_type]] = 1
        return one_hot_piezas.flatten()  # Combinar en un solo vector
    
    def combine_grid_and_piece(self):
        # Combinar el grid y la pieza en un array de forma (height, width, 2)
        combined = np.stack((self.grid, self.piece), axis=-1)
        return combined

    def update(self,piece:Piece, grid: list, next_pieces: deque, has_been_looked: bool):
        if(has_been_looked):
            self.next_pieces = self.transform_next_pieces(next_pieces)
            self.grid = np.array(grid)
            self.piece = self.transform_piece(piece)
        else:
            self.piece = self.transform_piece(piece)

    def get_input(self):
        combined_grid_piece = self.combine_grid_and_piece()
        return [combined_grid_piece, self.next_pieces]
    
    


    



