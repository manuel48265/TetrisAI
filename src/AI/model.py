import random
import tensorflow as tf
from keras import models, layers
import numpy as np
from collections import deque
from src.AI.preprocessing import Preprocessing
from src.utils.actions import Actions
from src.AI.tetrisEnviroment import TetrisEnviroment

class CNNmodel:
    def __init__(self,grid_shape, hot_vector_shape):
        self.grid_piece_shape = grid_shape
        self.hot_vector_shape = hot_vector_shape
        self.model = self.create_model(self.grid_piece_shape,self.hot_vector_shape)

    def create_model(self,input_shape_1, input_shape_2, dropout_rate=0.15):
        # Entradas
        input_x = layers.Input(shape=input_shape_1, name="input_x")
        input_y = layers.Input(shape=input_shape_1, name="input_y")
        input_vector = layers.Input(shape=input_shape_2, name="input_vector")

        # Procesamiento de input_x
        x = layers.Conv2D(32, (3, 3), activation='relu')(input_x)
        x = layers.Conv2D(64, (3, 3), activation='relu')(x)
        x_1 = layers.MaxPooling2D((2, 2))(x)
        x_2 = layers.AveragePooling2D((2,2))(x)
        x_1 = layers.Flatten()(x_1)
        x_2 = layers.Flatten()(x_2)

        # Procesamiento de input_y
        y = layers.Conv2D(32, (3, 3), activation='relu')(input_y)
        y = layers.Conv2D(64, (3, 3), activation='relu')(y)
        y_1 = layers.MaxPooling2D((2, 2))(y)
        y_2 = layers.AveragePooling2D((2,2))(y)
        y_1 = layers.Flatten()(y_1)
        y_2 = layers.Flatten()(y_2)

        # Procesamiento de input_vector
        vector_dense = layers.Dense(64, activation='relu')(input_vector)
        vector_dense = layers.LayerNormalization()(vector_dense)

        # Combinación de ramas
        combined = layers.concatenate([x_1,x_2,y_1, y_2,vector_dense])
        combined = layers.Dense(128, activation='relu')(combined)
        combined = layers.Dropout(dropout_rate)(combined)
        combined = layers.Dense(64, activation='relu')(combined)
        combined = layers.Dropout(dropout_rate)(combined)
        combined = layers.Dense(32, activation='relu')(combined)
        combined = layers.Dropout(dropout_rate)(combined)
        combined = layers.Dense(16, activation='relu')(combined)
        combined = layers.Dropout(dropout_rate)(combined)
        combined = layers.Dense(8, activation='relu')(combined)
        combined = layers.Dropout(dropout_rate)(combined)

        # Capa de salida
        output = layers.Dense(1, activation='linear')(combined)

        # Modelo
        model = models.Model(inputs={"input_x": input_x, "input_y": input_y, "input_vector": input_vector}, outputs=output)
        model.compile(optimizer='adam', loss='huber_loss', metrics=['mae'])

        return model


    def predict(self, input):
        result = self.model.predict(input, verbose=0,batch_size=64)
        return result

    def save(self, filepath):
        self.model.save(filepath)

    def fit(self, x_train, y_train, epochs, verbose=0):
        self.model.fit(x_train, y_train, epochs=epochs, verbose=0)

    def load(self, filepath):
        self.model = tf.keras.models.load_model(filepath)

    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test)




class DQLAgent:
    def __init__(self, model : CNNmodel, env : TetrisEnviroment, gamma=0.99, epsilon=1.0, epsilon_min=0.1, epsilon_decay=0.995, batch_size=128, memory_size=100000, rand_prob = 0.1, rand_prob_min = 0.01, rand_prob_decay = 0.995):
        self.model = model
        self.env = env
        self.gamma = gamma  # Factor de descuento
        self.epsilon = epsilon  # Probabilidad de exploración inicial
        self.epsilon_min = epsilon_min  # Valor mínimo de epsilon
        self.epsilon_decay = epsilon_decay  # Factor de disminución de epsilon
        self.batch_size = batch_size  # Tamaño del batch de entrenamiento
        self.memory = deque(maxlen=memory_size)  # Memoria de experiencias
        self.target_model = self._build_target_model()  # Modelo de objetivo
        self.rand_prob = rand_prob
        self.rand_prob_min = rand_prob_min
        self.rand_prob_decay = rand_prob_decay

    def _build_target_model(self):
        # Crea un modelo idéntico al modelo principal
        target_model = tf.keras.models.clone_model(self.model.model)
        target_model.set_weights(self.model.model.get_weights())
        return target_model

    def remember(self, state, reward, next_state, done):
        # Guarda la experiencia en la memoria
        self.memory.append((state, reward, next_state, done))

    def save(self, filepath):
        self.model.save(filepath)

    def load(self, filepath):
        self.model.load(filepath)
        self.target_model = self._build_target_model()

    def replay(self):
        pass
        

    def update_target_model(self):
        self.target_model.set_weights(self.model.model.get_weights())


    # Guardar experiencia
    # Guardar reward de experiencia 

    def get_next_move(self):
        self.env.calc_states()

    def train(self,episodes):
        self.env.start()

        

        for episode in range(episodes):
            self.env.reset()
            state = self.env.get_state()
            total_reward = 0
            done = False

            while not done:
                next_states, rewards, done, index = self.env.step()

                self.remember(state, rewards, next_states, done)
                #state = next_state
                #total_reward += reward
                
            self.replay()

            self.update_target_model()
            print(f"Episode: {episode + 1}, Total Reward: {total_reward}, Total Points {self.env.game.score} Epsilon: {self.epsilon:.2f}")


model = CNNmodel((20,10,2),(21,))




    




