from src.actions import Actions, get_action
class Player:
    
    def __init__(self,is_human, brain=None):
        self.is_human = is_human
        self.brain = brain

    def next_action(self):
        output = Actions.IDLE
        if(self.is_human):
            key = input().lower()
            return get_action(key)
        else:
            self.brain.get_action()



