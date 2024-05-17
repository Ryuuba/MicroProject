from test import test_wifi
from machine import Pin
from utime import sleep

def main() -> None:
    print('Maybe you want to test to code')

if __name__ == '__main__':
    interrupt_pin = Pin('GP1', Pin.IN, Pin.PULL_UP)
    if interrupt_pin.value() == 1:
        test_wifi()
    else:
        main()
