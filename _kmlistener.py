from uglimodules.kmhook import *
from uglimodules.timer import Timer

REPEAT_DURATION = 40
DOUBLE_PRESS_DURATION = 250
LONG_PRESS_DURATION = 500
AUTOREPEAT = 'autorepeat'
DOUBLE_PRESS = 'double press'
SIMPLE = 'simple'
ONCE = 'once'
RELEASE = 'release'
LINKED = 'linked'
DOUBLE_PRESS_AUTOREPEAT = 'double press autorepeat'
LONG_PRESS = 'long press'
debug = True
ALTERNATE_AUTOREPEAT = 'alternate autorepeat'


class Binding:

    def __init__(self, name: str = '', trigger_key='', mode: str = SIMPLE, duration=None, action_key=None,
                 category='generic',
                 priority=0):

        if isinstance(trigger_key, str):
            if trigger_key not in valid_key_names:
                raise ValueError(f'kmlistener : {trigger_key} is not a valid key name.')
        else:
            for key in trigger_key:
                if key not in valid_key_names:
                    raise ValueError(f'kmlistener : {key} is not a valid key name.')
        if action_key:
            if isinstance(action_key, str):
                if action_key not in valid_key_names:
                    raise ValueError(f'kmlistener : {action_key} is not a valid key name.')
            else:
                for key in action_key:
                    if key not in valid_key_names:
                        raise ValueError(f'kmlistener : {key} is not a valid key name.')

        self.is_on = True
        self.key_state = False
        self.key_state2 = False
        self.timer = None
        self.timer2 = None
        self.listen = None
        self.active = False
        self.duration = duration
        self.name = name
        self.trigger_key = trigger_key
        self.action_key = action_key
        self.category = category
        self.priority = priority
        self.mode = mode
        if mode == SIMPLE:
            self.listen = self.process_simple

        elif mode == ONCE:
            if isinstance(self.trigger_key, str):
                self.listen = self.process_once_simple
            else:
                self.listen = self.process_once_multiple

        elif mode == RELEASE:
            self.listen = self.process_release

        elif mode == AUTOREPEAT:
            self.timer = Timer(duration or REPEAT_DURATION)
            self.listen = self.process_autorepeat

        elif mode == DOUBLE_PRESS:
            self.timer = Timer(duration or DOUBLE_PRESS_DURATION)
            self.listen = self.process_double_press

        elif mode == LONG_PRESS:
            self.timer = Timer(duration or LONG_PRESS_DURATION)
            self.listen = self.process_long_press

        elif mode == LINKED:
            if isinstance(self.trigger_key, str):
                self.listen = self.process_linked
            else:
                self.listen = self.process_linked_multiple

        elif mode == DOUBLE_PRESS_AUTOREPEAT:
            self.timer = Timer(duration or DOUBLE_PRESS_DURATION)
            self.timer2 = Timer(REPEAT_DURATION)
            self.listen = self.double_press_autorepeat

        elif mode == ALTERNATE_AUTOREPEAT:
            self.timer = Timer(duration or REPEAT_DURATION)
            self.listen = self.process_alternate_autorepeat
            self.autorepeat_counter = 0
        Listener.bind(self)

    def set_on(self):
        self.is_on = True

    def set_off(self):
        self.is_on = False

    def process_simple(self):
        if is_pressed(self.trigger_key):
            self.post_event()
            return True
        else:
            return False

    def process_once_simple(self):

        if not self.key_state and is_pressed(self.trigger_key):
            self.post_event()
            self.key_state = True
            return True
        elif self.key_state and not is_pressed(self.trigger_key):
            self.key_state = False
            return False

    def process_once_multiple(self):

        if not self.key_state and are_pressed(self.trigger_key):
            self.post_event()
            self.key_state = True
            return True
        elif self.key_state and not are_pressed(self.trigger_key):
            self.key_state = False
            return False

    def process_release(self):
        if not self.key_state and is_pressed(self.trigger_key):
            self.key_state = True
            return False
        elif self.key_state and not is_pressed(self.trigger_key):
            self.key_state = False
            self.post_event()
            return True

    def process_autorepeat(self):
        result = False
        condition = is_pressed(self.trigger_key) if isinstance(self.trigger_key, str) else are_pressed(self.trigger_key)
        if condition:
            self.active = True
            if not self.key_state:
                self.key_state = True
                self.post_event()
                result = True
                self.timer.start()
            else:
                if self.timer.has_expired():
                    if self.action_key:
                        press_and_release(self.action_key)
                    self.post_event()
                    result = True
                    self.timer.start()
        else:
            self.active = False
            if self.key_state:
                self.key_state = False
                self.timer.stop()
        return result

    def process_alternate_autorepeat(self):
        result = False
        if is_pressed(self.trigger_key):
            self.active = True
            if not self.key_state:
                self.key_state = True
                self.post_event()
                result = True
                self.timer.start()
            else:
                if self.timer.has_expired():
                    if self.action_key:
                        press_and_release(self.action_key[self.autorepeat_counter])
                    self.post_event(self.autorepeat_counter)
                    self.autorepeat_counter = (self.autorepeat_counter + 1) % len(self.action_key)
                    result = True
                    self.timer.start()
        else:
            self.active = False
            if self.key_state:
                self.key_state = False
                self.timer.stop()
        return result

    def process_double_press(self):
        if self.key_state2 and is_pressed(self.trigger_key):
            return True
        self.key_state2 = False
        result = False
        if is_pressed_once(self.trigger_key):
            if not self.key_state or self.timer.has_expired():
                self.key_state = True
                self.timer.start()
            else:
                if self.action_key:
                    press_and_release(self.action_key)
                self.post_event()
                self.key_state = False
                self.key_state2 = True
                result = True

        return result

    def process_long_press(self):
        result = False
        if not self.key_state2:
            if is_pressed(self.trigger_key):
                if not self.key_state:
                    self.timer.start()
                    self.key_state = True
                elif self.timer.has_expired():
                    self.post_event()
                    result = True
                    self.key_state = False
                    self.key_state2 = True
                    self.timer.stop()
            else:
                if self.key_state:
                    self.timer.stop()
                    self.key_state = False
        else:
            if not is_pressed(self.trigger_key):
                self.key_state2 = False
        return result

    def process_linked(self):
        if not self.key_state and is_pressed(self.trigger_key):
            self.key_state = True
            self.active = True
            if self.action_key:
                press(self.action_key)
            self.post_event("pressed")
        elif self.key_state and not is_pressed(self.trigger_key):
            self.key_state = False
            self.active = False
            if self.action_key:
                release(self.action_key)
            self.post_event("released")
        return self.active

    def process_linked_multiple(self):
        if not self.key_state and are_pressed(self.trigger_key):
            self.key_state = True
            self.active = True
            if self.action_key:
                press(self.action_key)
            self.post_event("pressed")
        elif self.key_state and not are_pressed(self.trigger_key):
            self.key_state = False
            self.active = False
            if self.action_key:
                release(self.action_key)
            self.post_event("released")
        return self.active

    def double_press_autorepeat(self):
        result = False
        if not self.key_state2:
            if is_pressed_once(self.trigger_key):
                if not self.key_state or self.timer.has_expired():
                    self.key_state = True
                    self.timer.start()
                else:
                    if self.action_key:
                        press_and_release(self.action_key)
                    else:
                        self.post_event()
                        result = True
                    self.key_state = False
                    self.key_state2 = True
                    self.timer2.start()
                    self.active = True
                    self.timer.stop()
        else:
            if is_pressed(self.trigger_key) and self.timer2.has_expired():
                if self.action_key:
                    press_and_release(self.action_key)
                else:
                    self.post_event()
                    result = True
                self.timer2.start()
            elif not is_pressed(self.trigger_key):
                self.timer2.stop()
                self.key_state2 = False
                self.active = False
        return result

    def post_event(self, suffix=None):
        if not suffix:
            Listener.event_list.append(Event(self.name))
        else:
            Listener.event_list.append(Event(self.name + ':' + str(suffix)))

    def __repr__(self):
        return f'Binding(Name : {self.name} - Trigger : {self.trigger_key} - Mode : {self.mode} - Action Key : {self.action_key} - Category : {self.category} - Priority : {self.priority})'


class Event:
    def __init__(self, name):
        self.name = name


class Listener:
    event_list = []
    bindings = dict()

    def __init__(self):
        pass

    @staticmethod
    def set_category_off(category: str) -> None:
        if category not in Listener.bindings:
            raise ValueError(f"kmlistener : category {category} does not exist.")
        for binding in Listener.bindings[category]:
            binding.set_off()

    @staticmethod
    def set_category_on(category: str) -> None:
        if category not in Listener.bindings:
            raise ValueError(f"kmlistener : category {category} does not exist.")
        for binding in Listener.bindings[category]:
            binding.set_on()

    @staticmethod
    def set_off(name: str) -> None:
        for category in Listener.bindings:
            for binding in Listener.bindings[category]:
                if name in binding.name:
                    binding.set_off()
                    if debug:
                        print(f"{binding.name} is OFF")

    @staticmethod
    def set_on(name: str) -> None:
        for category in Listener.bindings:
            for binding in Listener.bindings[category]:
                if name in binding.name:
                    binding.set_on()
                    if debug:
                        print(f"{binding.name} is ON")

    @staticmethod
    def info():
        for b in Listener.bindings:
            print(f"Category {b}")
            for e in Listener.bindings[b]:
                print("\t\t" + str(e))

    @staticmethod
    def bind(binding: Binding):
        if debug:
            print(f"Binding {binding.name}")
            print(f"Category : {binding.category}")
            print(f"Priority : {binding.priority}")
        if binding.category in Listener.bindings:
            if debug:
                print("Categoriy exists")
            if binding.priority:
                for b in Listener.bindings[binding.category]:
                    if b.priority == binding.priority:
                        raise ValueError(
                            f'kmlistener : there is already a binding with priority {binding.priority} in category {binding.category}.')
            Listener.bindings[binding.category].append(binding)
            Listener.bindings[binding.category] = sorted(Listener.bindings[binding.category], reverse=True,
                                                         key=lambda x: x.priority)
        else:
            Listener.bindings[binding.category] = [binding]

    @staticmethod
    def event_get():
        while Listener.event_list:
            yield Listener.event_list.pop()

    @staticmethod
    def update():
        for category in Listener.bindings:
            for b in Listener.bindings[category]:
                if b.is_on and b.listen() and category != '':
                    break
