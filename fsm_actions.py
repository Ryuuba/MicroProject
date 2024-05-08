"""This module holds the actions associated to this project
"""

from utime import sleep_ms
from machine import Pin

def debounce_button(pin: Pin) -> None:
    cur_value = pin.value()
    active = 0
    while active < 20:
        if pin.value() != cur_value:
            active += 1
        else:
            active = 0
        sleep_ms(1)