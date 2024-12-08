import tensorflow as tf
from keras.src.models import Model
from keras.src.layers import Input, Conv2D, Flatten, Dense, Concatenate, GlobalAveragePooling2D, Reshape, BatchNormalization, Dropout
import numpy as np
from collections import deque
from preprocessing import Preprocessing

class CNNmodel:
    def __init__(self, grid_shape, num_actions, num_pieces):
        self.grid_piece_shape = grid_shape
        self.num_actions = num_actions
        self.num_pieces = num_pieces
        self.model = self.create_model()

    def create_model(self):
        # Entrada para el grid

        grid_input = Input(shape=self.grid_piece_shape, name='grid_input')
        
        # Primera convolución (3x3)
        x = Conv2D(32, (3, 3), activation='relu')(grid_input)
        x = BatchNormalization()(x)
        
        # Segunda convolución (2x2)
        x = Conv2D(256, (2, 2), activation='relu')(x)
        x = BatchNormalization()(x)
        
        # Tercera convolución (2x3)
        x = Conv2D(1024, (2, 3), activation='relu')(x)
        x = BatchNormalization()(x)
        
        # Cuarta convolución (sizex1)
        x = GlobalAveragePooling2D()(x)
        # Puede modificarse el tamaño para acelerar el entrenamiento
        x = Dense(1024, activation='relu')(x) # para ver las relaciones espaciales
        x = BatchNormalization()(x)


        # Entrada para el vector binario de las piezas
        binary_vector_input = Input(shape=(self.num_pieces * 3), name='binary_vector_input')
        # Preprocesado del vector binario para añadir información
        binary_vector_processed = Dense(128, activation='relu')(binary_vector_input)
        
        # Concatenar todas las entradas
        concatenated = Concatenate()([binary_vector_processed,x])
        
        # Capas densas
        z = Dense(512, activation='relu')(concatenated)
        z = Dropout(0.2)(z)
        z = Dense(128, activation='relu')(z)
        z = Dropout(0.2)(z)
        output = Dense(self.num_actions, activation='linear')(z)  # Predicción de la mejor acción
        
        model = Model(inputs=[grid_input, binary_vector_input], outputs=output)
        model.compile(optimizer='adam', loss='mse')
        return model

    def predict(self, inputs):
        return self.model.predict(inputs)

    def save(self, filepath):
        self.model.save(filepath)

    def load(self, filepath):
        self.model = tf.keras.models.load_model(filepath)

    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test)


