"""This module initializes the FSM used in this project (is not generic)
"""

from fsm import FSM

def init_fsm(fsm: FSM, event: dict[str, int]) -> None:
    """Set the transition rules of the FSM to be implemented

    Args:
        fsm (FSM): A non-initialized finite state machine 
    """
    fsm.set_transition_rule(0, event['unconditional'], 1)
    fsm.set_transition_rule(1, event['default'], 1)
    fsm.set_transition_rule(1, event['press button'], 2)
    fsm.set_transition_rule(1, event['timeout'], 3)
    fsm.set_transition_rule(2, event['button'], 4)
    fsm.set_transition_rule(2, event['not button'], 1)
    fsm.set_transition_rule(3, event['unconditional'], 5)
    fsm.set_transition_rule(4, event['unconditional'], 5)
    fsm.set_transition_rule(5, event['unconditional'], 1)
    fsm.compute_next_state(event['unconditional'])
    print('STATE 0 is done')
