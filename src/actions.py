from aenum import Enum
class Actions(Enum):
    IDLE = 0
    ROTATE = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4

key_to_action = {
    'w': Actions.ROTATE,
    'd': Actions.RIGHT,
    'a': Actions.LEFT,
    's': Actions.DOWN,
}

def get_action(key):
    return key_to_action(key)
    