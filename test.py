from trygger import *

# create a Trigger
trg = Trygger()


# decorate actions with appropriate trigger mode
@trg.on_double_press(key="z")
def replate():
    km.press_and_release("&")


@trg.on_double_press(key='s')
def reload():
    km.press_and_release("<")


# start all triggers
trg.start()

# do things
while not km.is_pressed("pause"):
    km.sleep(0.001)

# stop and wait for triggers to end
trg.stop()
trg.wait_and_quit()
