class IRQHandler:
    def __init__(self, fsm: FSM) -> None:
        """Overload constructor requiring the fsm that holds the transition rules. The methods here defined are ad hoc to a given microcontroller application

        Args:
            fsm (FSM): A FSM object that model a deterministic finite state machine
        """
        self.__fsm = fsm

    def 
