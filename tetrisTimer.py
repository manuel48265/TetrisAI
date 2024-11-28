import threading
import time

class TetrisTimer:
    """
    Timer to automatically trigger a piece drop after a certain time
    if no action is performed.
    """
    def __init__(self, timeout_seconds, on_timeout_callback):
        """
        Initializes the TetrisTimer.

        Args:
            timeout_seconds (int): The number of seconds before triggering the timeout action.
            on_timeout_callback (callable): A function to call when the timer times out.
        """
        self.timeout_seconds = timeout_seconds
        self.on_timeout_callback = on_timeout_callback
        self.timer_thread = None
        self.reset_event = threading.Event()
        self.running = False

    def start(self):
        """
        Starts the timer thread.
        """
        self.running = True
        self.timer_thread = threading.Thread(target=self._run_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def stop(self):
        """
        Stops the timer thread.
        """
        self.running = False
        self.reset_event.set()  # Ensure the thread exits if waiting
        if self.timer_thread:
            self.timer_thread.join()

    def reset(self):
        """
        Resets the timer to start counting again.
        """
        self.reset_event.set()  # Notify the thread to reset the timer

    def _run_timer(self):
        """
        Internal method to run the timer in a separate thread.
        """
        while self.running:
            self.reset_event.clear()
            is_reset = self.reset_event.wait(self.timeout_seconds)
            if not is_reset:  # Timer expired without a reset
                self.on_timeout_callback()  # Trigger the timeout action
