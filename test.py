"""This module holds test that evaluate the operation of this project
"""

from fsm import FSM
from random import randint
from utime import sleep
from machine import I2C, Pin, Timer, enable_irq, disable_irq
from ssd1306 import SSD1306_I2C
from irq_handler import press_button, timeout
from fsm_actions import init_fsm, debounce_button
from shared_obj import fsm, ev, digital_clock

def test_fsm_interrupt() -> None:
    """This module evaluates the correct operation of FSM objects
    """
    interrupt_state = disable_irq()
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    oled = SSD1306_I2C(128,64,i2c)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    button.irq(trigger=Pin.IRQ_FALLING, handler=press_button, hard=True)
    t = Timer() # create a timer object using timer 1
    t.init(mode=Timer.PERIODIC, period=1000, callback=timeout)
    init_fsm(fsm, ev)
    fsm.compute_next_state(ev['unconditional'])
    while True:
        state = fsm.get_current_state()
        if state == 1:
            pass
        elif state == 2:
            interrupt_state = disable_irq()
            button_val = debounce_button(button)
            if button_val == 0:
                fsm.compute_next_state(ev['button'])
            else:
                fsm.compute_next_state(ev['not button'])
        elif state == 3:
            digital_clock.clear_time()
            fsm.compute_next_state(ev['unconditional'])
        elif state == 4:
            oled.fill(0)
            h, m, s = digital_clock.get_time()
            oled.text(f'{h:02}:{m:02}:{s:02}', 0, 0)
            oled.show()
            enable_irq(interrupt_state)
            fsm.compute_next_state(ev['unconditional'])
        elif state == 5:
            interrupt_state = disable_irq()
            digital_clock.increment()
            fsm.compute_next_state(ev['unconditional'])
        else:
            print(f'Are you OK, Any?')
            break