from aenum import Enum
class Actions(Enum):
    ROTATE = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3
    IDLE = 4

    def __int__(self):
        return self.value
    
    @staticmethod
    def int_to_action(action: int):
        return Actions(action)



    