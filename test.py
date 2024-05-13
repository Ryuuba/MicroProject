"""This module holds test that evaluate the operation of this project
"""

from fsm import FSM
from fsm_init import init_fsm
from random import randint
from utime import sleep
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

def test_fsm()->None:
    """This module evaluates the correct operation of FSM objects
    """
    fsm = FSM()
    event = {
        'unconditional' : 0, 
        'default' : 1, 
        'press button' : 2, 
        'timeout' : 3, 
        'button' : 4, 
        'not button' : 5}
    init_fsm(fsm, event)
    while True:
        state = fsm.get_current_state()
        if state == 1:
            print(f'current state {state} = S1')
            rnd = randint(0, 2)
            if rnd == 0:
                fsm.compute_next_state(event['default'])
            elif rnd == 1:
                fsm.compute_next_state(event['timeout'])
            elif rnd == 2:
                fsm.compute_next_state(event['press button'])
        elif state == 2:
            print(f'current state {state} = S2')
            if randint(0, 1) == 0:
                fsm.compute_next_state(event['not button'])
            else:
                fsm.compute_next_state(event['button'])
        elif state == 3:
            print(f'current state {state} = S3')
            fsm.compute_next_state(event['unconditional'])
        elif state == 4:
            print(f'current state {state} = S4')
            fsm.compute_next_state(event['unconditional'])
        elif state == 5:
            print(f'current state {state} = S5')
            fsm.compute_next_state(event['unconditional'])
        else:
            print(f'current state {state}')
            break
        sleep(5)

def test_fsm_with_oled()->None:
    """This module evaluates the correct operation of FSM objects
    """
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    oled = SSD1306_I2C(128,64,i2c)
    fsm = FSM()
    event = {
        'unconditional' : 0, 
        'default' : 1, 
        'press button' : 2, 
        'timeout' : 3, 
        'button' : 4, 
        'not button' : 5}
    init_fsm(fsm, event)
    while True:
        state = fsm.get_current_state()
        if state == 1:
            oled.text(f'current state {state} = S1', 10, 0)
            rnd = randint(0, 2)
            if rnd == 0:
                fsm.compute_next_state(event['default'])
            elif rnd == 1:
                fsm.compute_next_state(event['timeout'])
            elif rnd == 2:
                fsm.compute_next_state(event['press button'])
        elif state == 2:
            oled.text(f'current state {state} = S2', 10, 0)
            if randint(0, 1) == 0:
                fsm.compute_next_state(event['not button'])
            else:
                fsm.compute_next_state(event['button'])
        elif state == 3:
            oled.text(f'current state {state} = S3', 10, 0)
            fsm.compute_next_state(event['unconditional'])
        elif state == 4:
            oled.text(f'current state {state} = S4', 10, 0)
            fsm.compute_next_state(event['unconditional'])
        elif state == 5:
            oled.text(f'current state {state} = S5', 10, 0)
            fsm.compute_next_state(event['unconditional'])
        else:
            print(f'current state {state}')
            break
        oled.show()
        sleep(5)
        oled.fill(0)
