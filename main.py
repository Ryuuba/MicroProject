from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep
from digital_clock import DigitalClock

def main() -> None:
    # init
    clock = DigitalClock(23,59,50)
    led = Pin("LED", Pin.OUT)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    button.irq(trigger=Pin.IRQ_RISING, handler=button_isr)
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    oled = SSD1306_I2C(128,64,i2c)

if __name__ == '__main__':
    main()