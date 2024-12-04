import pygame
import random
from src.gameControler import GameControler

# Colores
ROWS = 20
COLS = 10
CELL_SIZE = 40
DELTA = 20
BLACK =(0,0,0)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)

class UI:
    def __init__(self,size_x : int,size_y : int):
        self.screen = None
        self.width = size_x
        self.height = size_y
        self.level = 0
        self.score = 0
        self.background = None

    def start(self):
        #init the pygame
        pygame.init()
        #Create the surface, where I will put the elements
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.load_image()

    def draw_board(self):
        pass
    def draw_piece(self):
        pass
    def draw_panel(self,size,pos,color):
        new_panel = pygame.Surface((size))
        new_panel.fill(color)
        self.screen.blit(new_panel,pos)

    def update_view(game: GameControler):
        pass

    def rigth_panel(self):
        TITLE = pygame.font.Font(None, 40)
        COLS_NEXT = 4
        ROWS_NEXT = 12
        INIT_X = 1000
        INIT_Y = 50

        self.draw_panel((CELL_SIZE*COLS_NEXT + 2*DELTA,CELL_SIZE*ROWS_NEXT + 2*DELTA),(INIT_X - DELTA, INIT_Y - DELTA), BLACK)
        next_text = TITLE.render("NEXT", True, WHITE)

        self.screen.blit(next_text, (INIT_X + 2.2*DELTA, INIT_Y))  # Posicionar texto NEXT



    def left_panel(self,score,level):

        INIT_X = 105
        INIT_Y = 50
        MOVEMENT = 50
        self.draw_panel((2.5*MOVEMENT + 2*DELTA, 4*MOVEMENT + DELTA),(INIT_X - 2*DELTA,INIT_Y - DELTA),BLACK)
        # Fuente
        font_val = pygame.font.Font(None, 30)
        TITLE = pygame.font.Font(None, 40)

        # Crear textos

        score_text = TITLE.render("SCORE", True, WHITE)
        score_value = font_val.render(str(score),True, LIGHT_GRAY)
        level_text = TITLE.render("LEVEL", True, WHITE)
        level_value = font_val.render(str(level),True, LIGHT_GRAY)

        # Dibujar textos
        self.screen.blit(score_text, (INIT_X, INIT_Y))  # Posicionar texto SCORE
        self.screen.blit(score_value, (INIT_X, INIT_Y + MOVEMENT))  # Posicionar texto SCORE
        self.screen.blit(level_text, (INIT_X, INIT_Y + 2*MOVEMENT))  # Posicionar texto LEVEL
        self.screen.blit(level_value, (INIT_X, INIT_Y + 3*MOVEMENT))  # Posicionar texto LEVEL

    def load_image(self):
        # Cargar la imagen de fondo
        self.background = pygame.image.load("./images/BackGround2.jpeg")  

        # Escalar la imagen al tamaño de la ventana (opcional)
        self.background= pygame.transform.scale(self.background, (self.width, self.height))

    def central_panel(self):
        
        INIT_X = 400
        INIT_Y = 50

        self.draw_panel((CELL_SIZE*COLS + 2*DELTA,CELL_SIZE*ROWS + 2*DELTA),(INIT_X - DELTA, INIT_Y - DELTA), BLACK)

        for row in range(ROWS):
            for col in range(COLS):
                # Coordenadas de cada celda
                x = col * CELL_SIZE + INIT_X 
                y = row * CELL_SIZE + INIT_Y
                # Dibujar el contorno de cada celda
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.score += random.randint(0,10)
                        self.level += random.randint(0,10)
                if event.type == pygame.KEYUP:
                    pass


            self.screen.blit(self.background,(0,0))

            #self.draw_panel((40,40),(0,0))
            self.left_panel(self.score, self.level)
            self.rigth_panel()
            self.central_panel()


            pygame.display.update()
            
    

screen = UI(1280,910)
screen.start()
screen.run()

    

        

