"""This module holds the actions associated to this project
"""

from utime import sleep_ms, sleep
from machine import Pin
from digital_clock import DigitalClock
from ssd1306 import SSD1306_I2C
from machine import disable_irq, enable_irq
from fsm import FSM

def debounce_button(pin: Pin, delay: int = 20) -> int:
    """Filters by software the noise a push_button generates

    Args:
        pin (Pin): The pin where the push button is connected
    Source:
        https://docs.micropython.org/en/latest/pyboard/tutorial/debounce.html
    """
    cur_value = pin.value()
    active = 0
    while active < delay:
        if pin.value() != cur_value:
            active += 1
        else:
            active = 0
        sleep_ms(1)
    return cur_value

def keep_alive(led_pin: Pin) -> None:
    """blinks a led to signal the board is working

    Args:
        led_pin (Pin): An initialized pin that has attach a led
    """
    led_pin.toggle()
    sleep(1)
    print('Waitin\' for an event')


def update_clock(clock: DigitalClock) -> None:
    clock.increment()

def clear_clock(clock: DigitalClock) -> None:
    clock.clear_time()

def display_clock(clock: DigitalClock, oled: SSD1306_I2C) -> None:
    oled.fill(0)
    h, m, s = clock.get_time()
    time = f'{h:02}:{m:02}:{s:02}'
    oled.text(time, 10,0)
    oled.show()

def unknown_state():
    print('FALTA ERROR')

def init_fsm(fsm: FSM, event: dict[str, int]) -> None:
    """Set the transition rules of the FSM to be implemented

    Args:
        fsm (FSM): A non-initialized finite state machine 
    """
    fsm.set_transition_rule(0, event['unconditional'], 1)
    fsm.set_transition_rule(1, event['default'], 1)
    fsm.set_transition_rule(1, event['press button'], 2)
    fsm.set_transition_rule(1, event['timeout'], 5)
    fsm.set_transition_rule(2, event['button'], 3)
    fsm.set_transition_rule(2, event['not button'], 1)
    fsm.set_transition_rule(3, event['unconditional'], 4)
    fsm.set_transition_rule(4, event['unconditional'], 1)
    fsm.set_transition_rule(5, event['unconditional'], 4)