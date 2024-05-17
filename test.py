"""This module holds test that evaluate the operation of this project
"""

from fsm import FSM
from utime import sleep, sleep_ms
from machine import I2C, Pin, Timer, enable_irq, disable_irq
from ssd1306 import SSD1306_I2C
from irq_handler import press_button, timeout
from fsm_actions import init_fsm, read_button
import shared_obj
from dht import DHT11
import ahtx0

def test_oled() -> None:
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    oled = SSD1306_I2C(128,64,i2c)
    oled.text(f'You\'are safe here!!!', 0, 10)
    oled.show()

def test_dht11() -> None:
    dht_sensor = DHT11(Pin(18))
    while True:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        print(f'temp: {temp}, humidity: {hum}')
        sleep(5)

def test_AHT10() -> None:
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    sensor = ahtx0.AHT10(i2c)
    while True:
        print("\nTemperature: %0.2f C" % sensor.temperature)
        print("Humidity: %0.2f %%" % sensor.relative_humidity)
        sleep(5)

def test_fsm_interrupt() -> None:
    """This module evaluates the correct operation of FSM objects
    """
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    oled = SSD1306_I2C(128,64,i2c)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    button.irq(trigger=Pin.IRQ_FALLING, handler=press_button, hard=True)
    t = Timer() # create a timer object using timer 1
    t.init(mode=Timer.PERIODIC, period=1000, callback=timeout)
    init_fsm(shared_obj.fsm, shared_obj.ev)
    print(shared_obj.fsm.get_current_state())
    shared_obj.fsm.compute_next_state(shared_obj.ev['unconditional'])
    print('init OK')
    while True:
        state = shared_obj.fsm.get_current_state()
        if state == 1:
            h, m, s = shared_obj.digital_clock.get_time()
            time = f'{h:02}:{m:02}:{s:02}'
            oled.text(time, 0, 0)
            oled.show()
            if shared_obj.clear_display:
                oled.fill(0)
                shared_obj.clear_display = False
            shared_obj.fsm.compute_next_state(shared_obj.ev['default'])
            if shared_obj.debounce_button and read_button(button) == 0:
                shared_obj.debounce_button = False
                shared_obj.fsm.compute_next_state(shared_obj.ev['press button'])
        elif state == 2:
            # get time from server
            irq_state = disable_irq()
            shared_obj.digital_clock.clear_time()
            enable_irq(irq_state)
            shared_obj.fsm.compute_next_state(shared_obj.ev['unconditional'])
        else:
            print('Are you OK, Annie?')
            break