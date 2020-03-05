from itertools import cycle
import sys
from time import sleep
from threading import Event, Thread


class Spinner:
    phases = cycle(["⣾", "⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽"])

    def __init__(self):
        self.stop_running = Event()
        self.spin_thread = Thread(target=self.init_spin)

    def start(self):
        self.spin_thread.start()

    def stop(self):
        self.stop_running.set()
        self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stdout.write(next(self.phases))
            sys.stdout.flush()
            sleep(0.1)
            sys.stdout.write("\b")
