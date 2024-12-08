import threading
import time

class TetrisTimer:
    """
    A timer class that automatically triggers an action (piece drop) after
    a set period of inactivity in a Tetris game. The timer runs in a separate
    thread and can be reset or stopped as needed.

    Attributes:
        time (int): The number of seconds before triggering the timeout action.
        function (callable): A function to call when the timer times out.
        thread (threading.Thread): The thread responsible for running the timer.
        event (threading.Event): An event used to control the timer's execution.
    """
    
    def __init__(self, time: int, function=None):
        """
        Initializes the TetrisTimer instance.

        Args:
            time (int): The number of seconds before triggering the timeout action.
            function (callable, optional): A function to call when the timer times out.
                Defaults to None, which means no action will be triggered unless set later.
        """
        self.time = time
        self.function = function
        self.thread = None
        self.event = threading.Event()
        self.running = False

    def set_funct(self, function):
        """
        Sets or updates the function to be called when the timer times out.

        Args:
            function (callable): The function to call when the timer reaches its timeout.
        """
        self.function = function

    def start(self):
        """
        Starts the timer thread that will count down and trigger the action after the
        specified time period. The thread will continue running in the background.

        The `function` provided at initialization or via `set_funct` will be called
        when the timer times out.
        """
        if self.function is None:
            raise ValueError("Function to trigger on timeout must be set before starting the timer.")
        
        # Initialize the thread
        self.thread = threading.Thread(target=self._run)
        self.running = True
        self.thread.daemon = True  # Set as a daemon so it will exit when the main program exits
        self.thread.start()

    def stop(self):
        """
        Stops the timer thread. This will stop the timer and prevent any further timeout actions
        from being triggered.

        If the timer thread is still running, it will be joined to ensure it properly stops.
        """
        self.running = False
        self.reset()  # Ensure any ongoing wait is stopped
        if self.thread and self.thread.is_alive():
            self.thread = None

    def reset(self):
        """
        Resets the timer, canceling the current countdown. This will start the timer from the 
        beginning when the next timeout occurs. You can optionally set a new interval when resetting.

        The event is set to interrupt any ongoing wait.
        """
        self.event.set()  # Interrupt the current waiting state and reset the timer

    def _run(self):
        """
        Internal method to run the timer in a separate thread. It waits for the specified time period
        and then triggers the timeout action by calling the `function` provided at initialization or set later.

        The thread will keep running until the timer is stopped.
        """
        while self.running:
            self.event.wait(timeout=self.time)  # Wait for the specified time or until the event is set
            if not self.event.is_set():
                self.function()  # Call the function when the timer times out
            self.event.clear()  # Reset the event for the next timeout

    def reduce_time(self, interval: int):
        """
        Reduces the timeout period to a shorter interval. This can be used to make the piece drop faster,
        for example, as the game progresses.

        Args:
            interval (int): The new timeout period in seconds.
        """
        self.time = interval





