from test import test_fsm_interrupt, test_oled, test_dht11
from machine import Pin
from utime import sleep

def main() -> None:
    test_oled()
    sleep(10)

if __name__ == '__main__':
    interrupt_pin = Pin('GP1', Pin.IN, Pin.PULL_UP)
    if interrupt_pin.value() == 1:
        test_dht11()
    else:
        main()
