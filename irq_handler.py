from machine import Pin, Timer
from fsm import FSM
from utime import sleep_ms

class IRQHandler:
    def __init__(self, fsm: FSM, event: dict[str, int]) -> None:
        """Overload constructor requiring the fsm that holds the transition rules. The methods here defined are ad hoc to a given microcontroller application

        Args:
            fsm (FSM): A FSM object that model a deterministic finite state machine
        """
        self.__fsm : FSM = fsm
        self.__event : dict[str, int] = event

    def press_button(self, pin: Pin) -> None:
        """ IRQ executed when the push button is pressed

        Args:
            pin (Pin): The IRQ requieres a pin to perform some action with it (not needed in all cases)
        """
        # move to debounce button
        self.__fsm.compute_next_state(self.__event['press button'])

    def timeout(self, t : Timer) -> None:
        """IRQ executed when a timer rings

        Args:
            t (Timer): The IRQ requieres a timer to perform some action with it (not needed in all cases)
        """
        # move to debounce button
        self.__fsm.compute_next_state(self.__event['timeout'])
    
    


