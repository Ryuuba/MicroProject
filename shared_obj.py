from digital_clock import DigitalClock
from fsm import FSM

ev = {
    'unconditional' : 0, 
    'default' : 1, 
    'press button' : 2, 
    'button' : 3, 
    'not button' : 4,
    'timeout' : 5}

clear_display = False

debounce_button = False

temp_counter = 0

read_aht10 = False

fsm: FSM = FSM()

digital_clock: DigitalClock = DigitalClock()