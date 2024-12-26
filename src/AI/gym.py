from src.AI.model import CNNmodel, DQLAgent
from src.AI.preprocessing import Preprocessing
from src.AI.tetrisEnviroment import TetrisEnviroment
from src.utils.actions import Actions
import tensorflow as tf
import src.utils.pieceForm as pf
import time

model = CNNmodel((20,10,1), (21,))
env = TetrisEnviroment(100000, pf.pieces, (10,20), 3)

dqn = DQLAgent(model, env, epsilon=0.99)

dqn.train(1000)

dqn.save("model3.keras")





