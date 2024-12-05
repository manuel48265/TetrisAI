import threading
import time

class TetrisTimer:
    """
    Timer to automatically trigger a piece drop after a certain time
    if no action is performed.
    """
    def __init__(self, time, function=None):
        """
        Initializes the TetrisTimer.

        Args:
            timeout_seconds (int): The number of seconds before triggering the timeout action.
            on_timeout_callback (callable): A function to call when the timer times out.
        """
        self.time = time
        self.function = function
        self.thread = None
        self.event = threading.Event()

    def set_funct(self,function):
        self.function = function

    def start(self):
        """
        Starts the timer thread.
        """
        #Init the thread 
        self.thread = threading.Thread(target=self._run)
        #Boolean control variable
        self.running = True
        #Thread daemon for secondary tasks
        self.thread.daemon = True
        #Init the secondary thread
        self.thread.start()

    def stop(self):
        """
        Stops the timer thread.
        """
        self.running = False
        self.reset()
        if self.thread.is_alive():
            self.thread.join()

    def reset(self):
        """
        Reinicia el temporizador con un nuevo intervalo (opcional).
        :param interval: Nuevo intervalo en segundos (opcional).
        """
        self.event.set()  # Interrumpe el temporizador actual
        

    def _run(self):
        """
        Internal method to run the timer in a separate thread.
        """
        while self.running:
            self.event.wait(timeout=self.time)
            if not self.event.is_set():
                self.function()
            self.event.clear()

    def reduce_time(self,interval):
        """
            Documentation should be here. If I had documentation.
        """

        self.time = interval






