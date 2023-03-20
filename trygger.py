from threading import Thread

import km
from settings import *
from timer import Timer


class Trygger:
    def __init__(self):
        self.actions = []
        self.go_on = True

    def start(self):
        for action in self.actions:
            action.start()

    def stop(self):
        self.go_on = False

    def wait_and_quit(self):
        for action in self.actions:
            action.join()

    def on_pressed_once(self, key: str | list | tuple):
        def add_it(f):
            def wrapper(*args, **kwargs):
                while self.go_on:
                    km.sleep(0.001)
                    if km.is_pressed_once(key):
                        f(*args, **kwargs)

            self.actions.append(Thread(target=wrapper))
            return wrapper

        return add_it

    def on_double_press(self, key: str | list | tuple):
        def add_it(f):
            def wrapper(*args, **kwargs):
                timer = Timer(DOUBLE_PRESS_DURATION)
                already_pressed_once = False
                timer.start()
                while self.go_on:
                    km.sleep(0.001)
                    if km.is_pressed_once(key):
                        if not timer.has_expired():
                            f(*args, **kwargs)
                            already_pressed_once = False
                        else:
                            timer.start()
                            already_pressed_once = False

            self.actions.append(Thread(target=wrapper))
            return wrapper

        return add_it
