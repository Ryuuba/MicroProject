from machine import Pin, Timer
from fsm import FSM
import shared_obj


def press_button(pin: Pin) -> None:
    """ IRQ executed when the push button is pressed

    Args:
        pin (Pin): The IRQ requieres a pin to perform some action with it (not needed in all cases)
    """
    shared_obj.debounce_button = True

def timeout(t : Timer) -> None:
    """IRQ executed when a timer rings

    Args:
        t (Timer): The IRQ requieres a timer to perform some action with it (not needed in all cases)
    """
    shared_obj.digital_clock.increment()
    shared_obj.clear_display = True

def get_temp(t : Timer) -> None:
    """IRQ executed when a timer rings

    Args:
        t (Timer): The IRQ requieres a timer to perform some action with it (not needed in all cases)
    """
    shared_obj.temp_counter += 1
    if shared_obj.temp_counter == 300:
        shared_obj.read_aht10 = True
        shared_obj.temp_counter = 0

    


