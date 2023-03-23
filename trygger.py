from threading import Thread

from km import *
from settings import *
from timer import Timer
import ctypes


MessageBox = ctypes.windll.user32.MessageBoxW



class Trygger:
    def __init__(self):
        self.actions = []
        self.action_threads = []
        self.go_on = False

    def start(self,mainloop=False):
        self.go_on = True
        self.action_threads = [Thread(target=action) for action in self.actions]
        for action_thread in self.action_threads:
            action_thread.start()
        if mainloop:
            MessageBox(0, 'Click OK to quit', 'Trygger', 0)
            self.stop()
    def stop(self):
        self.go_on = False
        for action_thread in self.action_threads:
            action_thread.join()
        self.action_threads = []

    def on_single_press(self, key: str | list | tuple):
        def add_it(f):
            def wrapper(*args, **kwargs):
                while self.go_on:
                    sleep(0.001)
                    if is_pressed_once(key):
                        f(*args, **kwargs)

            self.actions.append(wrapper)
            return wrapper

        return add_it

    def on_double_press(self, key: str | list | tuple):
        def add_it(f):
            def wrapper(*args, **kwargs):
                timer = Timer(DOUBLE_PRESS_DURATION)
                already_pressed_once = False
                timer.start()
                while self.go_on:
                    sleep(0.001)
                    if is_pressed_once(key):
                        if not timer.has_expired():
                            f(*args, **kwargs)
                            already_pressed_once = False
                        else:
                            timer.start()
                            already_pressed_once = False

            self.actions.append(wrapper)
            return wrapper

        return add_it
