from threading import Thread

from kmhook import *

from settings import *
from timer import Timer

MessageBox = ctypes.windll.user32.MessageBoxW
timer = dict()
already_pressed_once = dict()


class Trygger:
    def __init__(self):
        self.single_press_actions = []
        self.double_press_actions = []
        self.action_threads = []
        self.go_on = False

    def start(self, mainloop=False):
        self.go_on = True
        self.action_threads = []
        self.action_threads.append(Thread(target=self.single_press_actions_process))
        self.action_threads.append(Thread(target=self.double_press_actions_process))
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
        if isinstance(key, list):
            key = tuple(key)

        def add_it(f):
            print(f, key)

            def wrapper(*args, **kwargs):
                if is_pressed_once(key):
                    f(*args, **kwargs)

            self.single_press_actions.append(wrapper)
            return wrapper

        return add_it

    def on_double_press(self, key: str | list | tuple):
        if isinstance(key, list):
            key = tuple(key)

        def add_it(f):  # fix that
            timer[key] = Timer(DOUBLE_PRESS_DURATION)
            already_pressed_once[key] = False
            timer[key].start()

            def wrapper(*args, **kwargs):

                if is_pressed_once(key):
                    if not timer[key].has_expired():
                        f(*args, **kwargs)
                        already_pressed_once[key] = False
                    else:
                        timer[key].start()
                        already_pressed_once[key] = True

            self.double_press_actions.append(wrapper)
            return wrapper

        return add_it

    def single_press_actions_process(self):
        while self.go_on:
            sleep(0.001)
            for action in self.single_press_actions:
                action()

    def double_press_actions_process(self):
        while self.go_on:
            sleep(0.001)
            for action in self.double_press_actions:
                action()
