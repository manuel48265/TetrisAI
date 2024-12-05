import pygame
from src.gameControler import GameControler
from src.UI import UI
from src.pieceForm import pieces
from src.player import Player

player = Player(False,idle=True)
juego = GameControler(0.3,pieces,player)
screen = UI(1280,910)
screen.start()
juego.start(10,20,3)

while juego.get_game_state():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.update(juego)

print(juego.get_score())


