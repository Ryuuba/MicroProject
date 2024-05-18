from test import test_fsm_interrupt, time_slave
from machine import Pin
from utime import sleep


def main() -> None:
    print('Maybe you want to test to code')

if __name__ == '__main__':
    interrupt_pin = Pin('GP1', Pin.IN, Pin.PULL_UP)
    if interrupt_pin.value() == 1:
        try:
            import network
        except ImportError:
            print('Running from a Rb Pico')
            test_fsm_interrupt()
        else:
            print('Running from a Rb Pico W')
            time_slave()
    else:
        main()
