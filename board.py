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
                    if(self.current_piece[posx][posy] == 1 ):
                        if(self.grid[posx][posy] != 0):
                            return True

        return False
    #end Subfunctions

    def set_new_piece(self, piece : Piece):
        valid_pos = False
        self.current_piece = Piece
        #Establecer posicion inicial en el centro del grid 
        self.current_piece.centre_on(self.width // 2,self.height - 1)

        if(not self.is_valid_position()):
            game_over = False
            i = 0
            while(not game_over and not valid_pos):
                if(self.current_piece.is_empty_row(i)):
                    self.current_piece.centre_on(self,self.height + i)
                    if(not self.is_valid_position()):
                        i+= 1
                    else:
                        valid_pos = True
                else: 
                    game_over = True

        return valid_pos
            
            


        
    
    def lock_piece(self):

        for i in range(self.current_piece.size()):
            for j in range(self.current_piece.size()):
                if(self.current_piece[i][j] == 1):
                    self.grid[self.current_piece.x + j][self.current_piece.y -i] == self.current_piece.get_color()

    def clear_lines(self,lines:list):
        total = 0

        for line in lines:

            for i in range(self.width):
                sum = 0
                if(self.grid[line][i] != 0):
                    sum += 1

            if(sum == len(self.grid[line])):
                total += 1
        
        return total
    
    def get_points_for_clear_lines(self,num_lines):
        return self.points[num_lines]
    
    def draw():
        pass