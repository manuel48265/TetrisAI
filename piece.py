import pieceForm as pf
import pygame
from constColors import tetris_colors
class Piece:
    def __init__(self,x: int, y:int, block: pf.PieceForm):
        self.x = x 
        self.y = y
        self.piece = block
    def move_right(self):
        self.x += 1
    def move_left(self):
        self.x -= 1
    def down(self):
        self.y -= 1
    def set_position(self,x:int,y:int):
        self.x = x 
        self.y = y
    #Hay que acabarla
    def centre_on(self,x:int,y:int):
        self.set_position(x - (self.piece.size-1) // 2,y)
    def __getitem__(self, key):
        return self.piece[key]
    def get_color(self):
        return self.piece.get_color()
    def size(self):
        return self.piece.size
    def is_empty_row(self, row:int):
        col = 0
        empty = True

        while(col < len(self.piece[row]) and empty):
            if(self.piece[row][col] != 0):
                empty = False
            col += 1
        
        return empty

    def draw(self,screen):
        for i in range(self.size()):
            for j in range (self.size()):
                if(self[i][j] == 1):
                    pygame.draw.rect(
                        screen,
                        tetris_colors(self.get_color()),
                        ((self.x + j) * self.CELL_SIZE, (self.y + i) * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                    )

        
