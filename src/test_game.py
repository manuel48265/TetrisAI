import pygame
import random
import time
from src.game import Game
from src.UI import UI
from src.utils.pieceForm import pieces
from src.controler import Controler
from src.utils.actions import Actions
from keras.src.losses import MeanSquaredError

from src.AI.model import CNNmodel
from src.AI.preprocessing import Preprocessing

controler = Controler(True)
juego = Game(1000,pieces)
screen = UI(1280,910)
screen.start()
juego.start(10,20,3)

#model = CNNmodel((20,10,2), 4, 7)
#preprocesor = Preprocessing(juego.get_board().get_grid(), juego.get_current_piece(), juego.get_next_pieces(), pieces)
#model.load("model3.keras")

import tensorflow as tf

# Listar dispositivos físicos
devices = tf.config.list_physical_devices('GPU')

if devices:
    for i, device in enumerate(devices):
        print(f"Dispositivo GPU {i}: {device.name}")
else:
    print("No se encontraron GPUs disponibles.")

while True:
    if juego.is_game_over():
        juego.reset()
        screen.update(juego)
    #screen.update(juego)
    #juego.update(controler.get_action())
    screen.update(juego)
    final_states, parents_map =juego.get_board().valid_future_positions_with_parents()
    state = random.choice(final_states)
    path = juego.get_board().get_path(state, parents_map)
    for action in path:
        juego.update(action)
        screen.update(juego)
    # Para poder cerrar la interfaz.
    controler.get_action()




