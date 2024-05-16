from digital_clock import DigitalClock
from fsm import FSM

ev = {
    'unconditional' : 0, 
    'default' : 1, 
    'press button' : 2, 
    'button' : 3, 
    'not button' : 4,
    'timeout' : 5}

fsm = FSM()

digital_clock = DigitalClock()