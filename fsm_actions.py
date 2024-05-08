"""This module holds the actions associated to this project
"""

from utime import sleep_ms, sleep
from machine import Pin
from digital_clock import DigitalClock
from ssd1306 import SSD1306_I2C
from machine import disable_irq, enable_irq

def debounce_button(pin: Pin, delay: int = 20) -> int:
    """Filters by software the noise a push_button generates

    Args:
        pin (Pin): The pin where the push button is connected
    Source:
        https://docs.micropython.org/en/latest/pyboard/tutorial/debounce.html
    """
    current_value = pin.value()
    active = 0
    while active < delay:
        if pin.value() != current_value:
            active += 1
        else:
            active = 0
        sleep_ms(1)
    return current_value

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