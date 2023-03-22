# Trygger


## Purpose

Trygger is an easy-to-use Windows only python app.

It helps you decorate functions so that they are called when a key (or a sequence of keys) is pressed once or twice.

The decorated function is placed in a separated thread periodically checking for keys pressed.

Trygger relies on `km`, which is a small module dedicated to 
- detect keyboard and mouse events ;
- synthesize keyboard and mouse events ;
- create continuous mouse movements.

## Usage

```python
import trygger as tg

# create a Trigger
trg = tg.Trygger()


# decorate actions with appropriate trigger mode
@trg.on_double_press(key='space')
def press_a_key():
    tg.press_and_release('escape')


# trigger can be a sequence of keys
@trg.on_single_press(('lctrl', 's'))
def print_something():
    print("you pressed Left Control + Space.")


# start all triggers
trg.start()

# do things
while not tg.is_pressed("pause"):
    tg.sleep(0.001)

# stop and wait for triggers to end
trg.stop()
```

