import trygger as tg

# create a Trigger
trg = tg.Trygger()


# decorate actions with appropriate trigger mode
@trg.on_single_press(key='space')
def foo():
    print("You just pressed space")


# start all triggers
trg.start(mainloop=True)

# exiting MessageBox will stop Trygger
