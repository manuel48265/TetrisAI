import pytest
import time
from src.tetrisTimer import TetrisTimer

class TClass:
    def __init__(self):
        self.vector = []

    def testfunction(self):
        self.vector.append(1)

@pytest.mark.parametrize(
    "seconds,num",
    [
        (0.1,4),
        (0.2,5),
        (0.05,10)
    ]
)

def test_start(seconds,num):
    tester = TClass()
    target =[1 for i in range(num)]

    timer = TetrisTimer(seconds,tester.testfunction)
    

    timer.start()

    time.sleep(seconds*num + seconds*num/10)

    timer.stop()

    assert tester.vector == target

@pytest.mark.parametrize(
    "seconds,num",
    [
        (0.3,4),
        (0.2,6),
        (0.05,10)
    ]
)
def test_reset(seconds,num):
    tester = TClass()
    target =[1 for i in range(num//2)]

    timer = TetrisTimer(seconds,tester.testfunction)

    timer.start()

    for i in range(num):
        if i%2 == 0:
            timer.reset()
        else: 
            time.sleep(seconds + seconds /10)
    
    assert tester.vector == target








    







