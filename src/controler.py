import pygame
from src.utils.actions import Actions
class Controler:
    def __init__(self,is_human=None):
        self.is_human = is_human

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

            