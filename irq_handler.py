from machine import Pin, Timer
from fsm import FSM
from shared_obj import fsm, ev


def press_button(pin: Pin) -> None:
    """ IRQ executed when the push button is pressed

    Args:
        pin (Pin): The IRQ requieres a pin to perform some action with it (not needed in all cases)
    """
    # move to debounce button
    fsm.compute_next_state(ev['press button'])

def timeout(t : Timer) -> None:
    """IRQ executed when a timer rings

    Args:
        t (Timer): The IRQ requieres a timer to perform some action with it (not needed in all cases)
    """
    fsm.compute_next_state(ev['timeout'])
    


