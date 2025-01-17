import pygame
import random
import time
import threading
import subprocess
import copy
import multiprocessing
from src.UI import UI
from src.utils.pieceForm import pieces
from src.controler import Controler
from src.utils.actions import Actions
from src.AI.GeneticModels import GeneticModels

from src.AI.tetrisEnviroment import TetrisEnviroment



#model = CNNmodel((20,10,2), 4, 7)
#preprocesor = Preprocessing(juego.get_board().get_grid(), juego.get_current_piece(), juego.get_next_pieces(), pieces)
#model.load("model3.keras")

def play_game(times : int, model: list) -> int:

    entorno = TetrisEnviroment(1000,pieces,(10,20),3)
    entorno.start()

    vals = []
    holes_arr = []
    avg_heigth_arr = []
    sum_holes = 0
    sum_avg_heigth = 0
    count = 0

    for _ in range(times):
        while True:
            if entorno.game.is_game_over():
                print("points", entorno.game.score)
                vals.append(entorno.game.score)
                print("holes:", sum_holes/count)
                holes_arr.append(sum_holes/count)
                avg_heigth_arr.append(sum_avg_heigth/count)
                print("avg_heigth:",sum_avg_heigth/count)
                entorno.reset()
                break
            count+=1
            state,holes,avg_heigth = entorno.get_max_heuristic_model(model)
            path = entorno.get_path(state)
            sum_holes += holes
            sum_avg_heigth += avg_heigth

            for action in path:
                entorno.game.update(action)

    result = 0

    for i in range(len(vals)):
        aux = (1 - 0.02*avg_heigth_arr[i] - 0.01*holes_arr[i])
        if  aux < 0:
            result += 0
        else:
            result += (aux**2)*vals[i]

    result = result/len(vals)

    return result

    
    

print("How do you want to play?")
print("1. Manual")
print("2. AI with UI")
print("3. AI without UI")
print("4. Genetic Algorithm")
print("5. Genetic Algortihm result with UI")

mode = input("Select mode: ")



if mode == "1" or mode == "2" or mode == "5":
    controler = Controler(True)
    #juego = Game(1000,pieces)
    screen = UI(1280,910)
    screen.start()
    #juego.start(10,20,3)

if mode == "1":

    entorno = TetrisEnviroment(1,pieces,(10,20),3)
    entorno.start()

    while True:
        if entorno.game.is_game_over():
            entorno.reset()
            screen.update(entorno.game)
        screen.update(entorno.game)
        entorno.game.update(controler.get_action())
        screen.update(entorno.game)

elif mode == "2":

    entorno = TetrisEnviroment(1000,pieces,(10,20),3)
    entorno.start()

    while True:
        if entorno.game.is_game_over():
            entorno.reset()
            screen.update(entorno.game)
        #screen.update(juego)
        #juego.update(controler.get_action())
        screen.update(entorno.game)

        state = entorno.get_max_heuristic()
        path = entorno.get_path(state)
        for action in path:
            entorno.game.update(action)
            screen.update(entorno.game)
            #time.sleep(0.03)
        # Para poder cerrar la interfaz.
        controler.get_action()

elif mode == "3":

    entorno = TetrisEnviroment(1000,pieces,(10,20),3)
    entorno.start()

    while True:

        if entorno.game.is_game_over():
            print(entorno.game.score)
            entorno.reset()

        state = entorno.get_max_heuristic()
        path = entorno.get_path(state)

        for action in path:
            entorno.game.update(action)

elif mode == "4":


    NUM_PROCESSES = 12
    objective = 500000
    best_value = 0
    biggest_value = 0
    best_model = None

    # Resultados que serán compartidos entre procesos

    manager = multiprocessing.Manager()
    results = manager.list([0] * NUM_PROCESSES)

    print(results)

    generator = GeneticModels(NUM_PROCESSES, 0.2, 0.9, 0.02, 0.5, [(21, 8), (16, 8), (16, 1)])
    population = generator.init_population()
    #generator.load("120000.txt")
    #population[0] = copy.deepcopy(generator.best_model)

    # Función que ejecuta el juego y actualiza el resultado en un proceso
    def play_game_process(i, chromosome, results):
        result = play_game(1, chromosome)
        results[i] = result

    # Inicialización de los procesos
    while best_value < objective:
        processes = []

        # Crear y comenzar los procesos
        for i in range(NUM_PROCESSES):
            process = multiprocessing.Process(target=play_game_process, args=(i, population[i], results))
            processes.append(process)
            process.start()

        # Mientras los procesos están en ejecución, se puede evolucionar la población
        for process in processes:
            process.join()  # Espera a que todos los procesos terminen

        # Actualizar el mejor valor y la población
        best_value = max(results)
        print(f"Best value: {best_value}")
        print(results)

        if best_value > biggest_value:
            biggest_value = best_value
            best_index = results.index(best_value)
            generator.best_model = population[best_index]
            generator.save("best_model.txt")

        population = generator.next_generation(population, results)
        population[0] = copy.deepcopy(generator.best_model)

    # Identificar el índice del mejor modelo
    best_index = results.index(best_value)

    # Guardar el mejor modelo después de alcanzar el objetivo
    generator.best_model = population[best_index]
    generator.save("best_model_d.txt")

elif mode == "5":
    entorno = TetrisEnviroment(1000,pieces,(10,20),3)
    entorno.start()

    generator = GeneticModels(10, 0.6, 0.9, 0.02, 0.5,[(21, 8), (16, 8), (16, 1)])
    generator.load("Models/850000.txt")
    #print(play_game(1,generator.best_model))

    while True:
        if entorno.game.is_game_over():
            print(entorno.game.score)
            entorno.reset()
            screen.update(entorno.game)
        #screen.update(juego)
        #juego.update(controler.get_action())
        screen.update(entorno.game)

        state,holes,avg_height = entorno.get_max_heuristic_model(generator.best_model)
        path = entorno.get_path(state)

        for action in path:
            entorno.game.update(action)
            screen.update(entorno.game)
            #time.sleep(0.01)
        # Para poder cerrar la interfaz.
        controler.get_action()




        

    






