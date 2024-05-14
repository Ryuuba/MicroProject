from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
from utime import sleep
from digital_clock import DigitalClock
from fsm import FSM
from irq_handler import IRQHandler
import fsm_actions
from machine import disable_irq, enable_irq
from fsm_init import init_fsm
from test import test_fsm_with_button


def main() -> None:
    # init state
    fsm = FSM()
    event = {
        'unconditional' : 0, 
        'default' : 1, 
        'press button' : 2, 
        'timeout' : 3, 
        'button' : 4, 
        'not button' : 5}
    init_fsm(fsm, event)
    irq_handler = IRQHandler(fsm, event)
    clock = DigitalClock(23,59,50)
    led = Pin("LED", Pin.OUT)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    button.irq(trigger=Pin.IRQ_RISING, handler=irq_handler.press_button)
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    oled = SSD1306_I2C(128,64,i2c)
    t = Timer() # create a timer object using timer 1
    t.init(mode=Timer.PERIODIC, period=1000, callback=irq_handler.timeout) # initialize it in periodic mode
    # unconditionally, passes the the next state 'cause init is done
    fsm.compute_next_state(event['unconditional'])
    irq_state = disable_irq()
    print('init is OK')
    while True:
        state = fsm.get_current_state()
        if state == 1:
            print(f'current state {state}')
            # enable_irq(irq_state)
            led.toggle()
            sleep(1)
            print('Waitin\' for an event')
            fsm.compute_next_state(event['default'])
            print(f'Next state: {fsm.get_current_state()}')
            # Other events are controlled by the interrupt handler
        elif state == 2:
            print(f'current state {state}')
            irq_state = disable_irq()
            button_val = fsm_actions.debounce_button(button)
            if button_val == 0:
                fsm.compute_next_state(event['button'])
            else:
                fsm.compute_next_state(event['not button'])
        elif state == 3:
            print(f'current state {state}')
            irq_state = disable_irq()
            fsm_actions.update_clock(clock)
            fsm.compute_next_state(event['unconditional'])
        elif state == 4:
            print(f'current state {state}')
            irq_state = disable_irq()
            fsm_actions.clear_clock(clock)
            fsm.compute_next_state(event['unconditional'])
        elif state == 5:
            print(f'current state {state}')
            irq_state = disable_irq()
            fsm_actions.display_clock(clock, oled)
        else:
            print(f'current state {state}')
            fsm_actions.unknown_state()
            break
            

if __name__ == '__main__':
    debug = True
    if debug:
        test_fsm_with_button()
    else:
        main()
