import pygame
import src.pieceForm as pf
from src.constColors import tetris_colors
class Piece:
    def __init__(self,x: int, y:int, block: pf.PieceForm = None):
        self.x = x 
        self.y = y
        self.piece = block

    def rotate(self):
        self.piece.rotate()

    def unrotate(self):
        self.piece.unrotate()

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def up(self):
        self.y += 1

    def down(self):
        self.y -= 1

    def set_position(self,x:int,y:int):
        self.x = x 
        self.y = y

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

        if(row < self.size()):
            while(col < len(self.piece[row]) and empty):
                if(self.piece[row][col] != 0):
                    empty = False
                col += 1
        else:
            raise RuntimeError("row out of limits")
            
        
        return empty
    
    def adjust_pos(self, sizex: int):
        posx = self.x

        if(posx < 0):
            posx = 0
        if(posx + self.size() > sizex):
            posx = sizex - self.size()

        self.set_position(posx,self.y)

    def get_lines(self):
        output = []
        lower_bound = 0
        upper_bound = self.y + 1
        if(self.y - self.size() + 1 >= 0):
            lower_bound = self.y - self.size() + 1 

        for i in range(lower_bound,upper_bound):
            output.append(i)

        return output


    def draw(self,screen):
        for i in range(self.size()):
            for j in range (self.size()):
                if(self[i][j] == 1):
                    pygame.draw.rect(
                        screen,
                        tetris_colors(self.get_color()),
                        ((self.x + j) * self.CELL_SIZE, (self.y + i) * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                    )



