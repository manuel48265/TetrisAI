import pytest
import time
from src.utils.tetrisTimer import TetrisTimer

class TClass:
    """
    A helper class for testing purposes that contains a vector and a method
    to append an element to the vector when called.
    """
    def __init__(self):
        """
        Initializes an empty vector to store values for testing.
        """
        self.vector = []

    def testfunction(self):
        """
        Appends the value 1 to the vector when called. This method is used 
        as a callback for the TetrisTimer class.
        """
        self.vector.append(1)

@pytest.mark.parametrize(
    "seconds,num",
    [
        (0.1, 4),  # Test with 0.1 seconds interval and 4 expected invocations.
        (0.2, 5),  # Test with 0.2 seconds interval and 5 expected invocations.
        (0.05, 10)  # Test with 0.05 seconds interval and 10 expected invocations.
    ]
)
def test_start(seconds, num):
    """
    Test to verify that the timer correctly triggers the function at the expected 
    intervals and the correct number of times.

    This test creates an instance of TetrisTimer and checks that the function 
    is called the expected number of times (as indicated by `num`) after the 
    specified `seconds` interval.

    Parameters:
    - seconds: The time interval (in seconds) between each function call.
    - num: The expected number of times the function should be called.
    """
    tester = TClass()  # Create an instance of TClass to store the results.

    # Generate the expected result list of 1's.
    target = [1 for _ in range(num)]  

    timer = TetrisTimer(seconds, tester.testfunction)  # Create a TetrisTimer instance.

    timer.start()  # Start the timer.

    # Wait for the expected duration (num * seconds) plus a small buffer to ensure timing.
    time.sleep(seconds * num + seconds * num / 10)

    timer.stop()  # Stop the timer.

    # Assert that the function was called the expected number of times.
    assert tester.vector == target  # Verify the vector matches the expected result.


@pytest.mark.parametrize(
    "seconds,num",
    [
        (0.3, 4),  # Test with 0.3 seconds interval and 4 expected invocations.
        (0.2, 6),  # Test with 0.2 seconds interval and 6 expected invocations.
        (0.05, 10)  # Test with 0.05 seconds interval and 10 expected invocations.
    ]
)
def test_reset(seconds, num):
    """
    Test to verify that the timer correctly resets and only triggers the function 
    after the reset condition.

    This test checks that when the timer is reset during its countdown, the function 
    only gets triggered the expected number of times (half of the total invocations in this case).

    Parameters:
    - seconds: The time interval (in seconds) between each function call.
    - num: The total number of expected invocations of the function.
    """
    tester = TClass()  # Create an instance of TClass to store the results.

    # Generate the expected result list of 1's after half the total invocations (due to resets).
    target = [1 for _ in range(num // 2)]  

    timer = TetrisTimer(seconds, tester.testfunction)  # Create a TetrisTimer instance.

    timer.start()  # Start the timer.

    # Perform a mix of reset and wait actions based on the test case.
    for i in range(num):
        if i % 2 == 0:  # Reset the timer for every even iteration.
            timer.reset()
        else:  # For odd iterations, wait a bit before the next action.
            time.sleep(seconds + seconds / 10)

    # Assert that the function was called only the expected number of times after resets.
    assert tester.vector == target  # Verify the vector matches the expected result.










    







