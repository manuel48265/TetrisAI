import pygame
import time
from src.game import Game
from src.UI import UI
from src.utils.pieceForm import pieces
from src.controler import Controler

controler = Controler(True)
juego = Game(0.5,pieces)
screen = UI(1280,910)
screen.start()
juego.start(10,20,3)

while juego.get_game_state():
    screen.update(juego)
    juego.update(controler.get_action())

while True:
    controler.get_action()


