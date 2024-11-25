from piece import Piece
class Board:
    def __init__(self, width : int, height: int):
        self.width = width
        self.height = height
        self.grid = [[0 for i in range(width)] for i in range(height)]
        self.current_piece = None
        self.points ={1:100,2:300,3:500,4:800}
    #If the piece can move to the rigth, left, or can rotate.
    def is_valid_position(self):
        return (not self.out_of_limits() and not self.piece_colide())

    #begin Subfunctions
    def out_of_limits(self):

        for i in range(self.current_piece.size()):
            for j in range(self.current_piece.size()):
                if(self.current_piece[i][j] == 1):
                    if(self.current_piece.posx + j > self.width):
                        return True
                    elif(self.current_piece.posy -i < 0):
                        return True
                    
        return False

    def piece_colide(self):

        for i in range(self.current_piece.size()):
            for j in range(self.current_piece.size()):
                if(self.current_piece[i][j] == 1):
                    posx = self.current_piece.posx + j
                    posy = self.current_piece.posy - i
                    if(self.current_piece[posx][posy] == 1 and self.grid[posx][posy] != 0):
                        return True

        return False
    #end Subfunctions

    def new_piece(self, piece : Piece):
        self.current_piece = Piece
        #Establecer posicion aleatoria en el inicio del grid 
        #Ongoing
        self.current_piece.set_position(self,self.height)
    
    def lock_piece(self):

        for i in range(self.current_piece.size()):
            for j in range(self.current_piece.size()):
                if(self.current_piece[i][j] == 1):
                    self.grid[self.current_piece.x + j][self.current_piece.y -i] == self.current_piece.get_color()


        

    def clear_lines(self,lines:list):
        sum = 0

        for line in lines:
            for i in range(self.width):
                if(self.grid[line][i] != 0):
                    sum += 1
        
        return sum
    
    def get_points_for_clear_lines(self,num_lines):
        return self.points[num_lines]
    
    def draw():
        pass