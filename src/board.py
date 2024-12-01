from src.piece import Piece

class Board:
    def __init__(self, width : int, height: int):
        self.width = width
        self.height = height
        self.grid = [[0 for i in range(width)] for i in range(height)]
        self.current_piece = None
        self.points ={0:0,1:100,2:300,3:500,4:800}
            
    #If the piece can move to the rigth, left, or can rotate.

    def is_valid_position(self):

        for i in range(self.current_piece.size()):
            for j in range(self.current_piece.size()):
                if(self.current_piece[i][j] == 1):
                    posx = self.current_piece.x + j
                    posy = self.current_piece.y + i
                    bad_x = posx >= self.width or posx < 0
                    bad_y = posy < 0 or posy > self.height
                    if(bad_x or bad_y):
                        return False
                    elif(self.grid[posy][posx] != 0):
                        return False
        return True

    def _cols_down(self, lines: list):
        current_line = next_line = self.height - 1

        while (next_line >= 0):

            while (next_line in lines):
                next_line-=1

            if(next_line >= 0):
                self.grid[current_line] = next_line

            current_line-=1
            next_line -= 1

        for i in range(len(lines)):
            self.grid[i] = self.width *[0]


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
                    self.current_piece.centre_on(self,self.height - i)
                    if(not self.is_valid_position()):
                        i+= 1
                    else:
                        valid_pos = True
                else: 
                    game_over = True

        return valid_pos
    

    def rotate_piece(self):
        output = True
        pos_x,pos_y = self.current_piece.x,self.current_piece.y

        self.current_piece.adjust_pos(self.width,self.height)
        self.current_piece.rotate()

        if(not self.is_valid_position()):
            output = False
            self.current_piece.unrotate()
            self.current_piece.set_position(pos_x,pos_y)
            
        return output

    def move_piece_down(self):
        output = True
        self.current_piece.down()

        if(self.piece_colide()):
            self.current_piece.up()
            self.lock_piece()
            output = False
        
        return output
    
    def move_piece_rigth(self):
        output = True
        self.current_piece.move_right()

        if(not self.is_valid_position()):
            self.current_piece.move_left()
            output = False

        return output


    def move_piece_left(self):
        output = True
        self.current_piece.move_left()

        if(not self.is_valid_position()):
            self.current_piece.move_right()
            output = False

        return output

    def lock_piece(self):
        
        for i in range(self.current_piece.size()):
            for j in range(self.current_piece.size()):
                if(self.current_piece[i][j] == 1):
                    self.grid[self.current_piece.x + j][self.current_piece.y -i] == self.current_piece.get_color()

        
    def update_and_return_points(self):
        self.lock_piece()
        lines = self.current_piece.get_lines()
        lines = self.identify_lines(lines)
        self._cols_down(lines)
        return self._get_points_for_clear_lines(len(lines))


    def identify_lines(self,lines:list):
        total = []

        for line in lines:
            sum = 0
            for i in range(self.width):
                if(self.grid[line][i] != 0):
                    sum += 1

            if(sum == len(self.grid[line])):
                total.append(line)
        
        return total
    
    def _get_points_for_clear_lines(self,num_lines):
        return self.points[num_lines]
    
    def draw():
        pass