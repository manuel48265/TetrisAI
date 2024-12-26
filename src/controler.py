import pygame
from src.utils.actions import Actions
import numpy as np
class Controler:
    def __init__(self,is_human=None,model=None):
        self.is_human = is_human
        self.model = model

    def get_action(self):

        if(self.is_human):
            
            action = Actions.IDLE

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_a:
                        action = Actions.LEFT
                    if event.key == pygame.K_d:
                        action = Actions.RIGHT
                    if event.key == pygame.K_w:
                        action = Actions.ROTATE
                    if event.key == pygame.K_s:
                        action = Actions.DOWN

            return action
        

    def get_AI_Action(self,game_state):
        return Actions.int_to_action(np.argmax(self.model.predict(game_state)))




            