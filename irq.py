from machine import Pin, Timer
from fsm import FSM
from utime import sleep_ms

class IRQHandler:
    def __init__(self, fsm: FSM) -> None:
        """Overload constructor requiring the fsm that holds the transition rules. The methods here defined are ad hoc to a given microcontroller application

        Args:
            fsm (FSM): A FSM object that model a deterministic finite state machine
        """
        self.__fsm = fsm

    def press_button(self, pin: Pin) -> None:
        """ IRQ execute when the push button is pressed

        Args:
            pin (Pin): The IRQ requieres a pin to performed some action with it (not needed in all cases)
        """
        self.__fsm.compute_next_state('press_button')
        # move to debounce button

    
    


