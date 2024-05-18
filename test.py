"""This module holds test that evaluate the operation of this project
https://forums.raspberrypi.com/viewtopic.php?t=302978
"""

from fsm import FSM
from utime import sleep, sleep_ms
from machine import I2C, Pin, Timer, enable_irq, disable_irq
from ssd1306 import SSD1306_I2C
from irq_handler import press_button, timeout, get_temp
from fsm_actions import init_fsm, read_button
import shared_obj
from dht import DHT11
import ahtx0
from machine import UART

def time_slave() -> None:
    uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))
    test_wifi()
    try:
        while True:
            if uart.any():
                uart.read(1)
                dt = get_time_from_server()
                print(dt)
                uart.write(dt)
    except KeyboardInterrupt:
        pass

def get_time_from_server() -> bytes:
    import socket
    host = "192.168.1.84"  # Replace with the server's IP address
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    server_time = b'00-00-00 00:00:00'
    try:
        server_time = client_socket.recv(1024)
    except Exception as e:
        print(f"Error receiving data: {e}")
    finally:
        client_socket.close()
    return server_time

def test_wifi() -> None:
    import network
    ssid = 'labred'
    password = 'labred2017'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
    print('Connected to WiFi!')
    print('IP address:', wlan.ifconfig()[0])

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
    uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    oled = SSD1306_I2C(128,64,i2c)
    button = Pin(15, Pin.IN, Pin.PULL_UP)
    button.irq(trigger=Pin.IRQ_FALLING, handler=press_button, hard=True)
    t_clock = Timer() # create a timer object using timer 1
    t_clock.init(mode=Timer.PERIODIC, period=1000, callback=timeout)
    t_temp = Timer() # create a timer object using timer 1
    t_temp.init(mode=Timer.PERIODIC, period=1000, callback=get_temp)
    sensor = ahtx0.AHT10(i2c)
    temp = f'Temp: {sensor.temperature:0.2f}.C'
    hum = f'Hum: {sensor.relative_humidity:0.2f}%'
    init_fsm(shared_obj.fsm, shared_obj.ev)
    print(shared_obj.fsm.get_current_state())
    shared_obj.fsm.compute_next_state(shared_obj.ev['unconditional'])
    print(i2c.scan())
    print('init OK')
    while True:
        state = shared_obj.fsm.get_current_state()
        if state == 1:
            h, m, s = shared_obj.digital_clock.get_time()
            time = f'{h:02}:{m:02}:{s:02}'
            date = f'2024-05-17'
            oled.text(time, 0, 0)
            oled.text(date, 0, 10)
            oled.text(temp, 0, 20)
            oled.text(hum, 0, 30)
            oled.show()
            if shared_obj.read_aht10:
                temp = f'Temp: {sensor.temperature:0.2f}.C'
                hum = f'Hum: {sensor.relative_humidity:0.2f}%'
                shared_obj.read_aht10 = False
            if shared_obj.clear_display:
                oled.fill(0)
                shared_obj.clear_display = False
            shared_obj.fsm.compute_next_state(shared_obj.ev['default'])
            if shared_obj.debounce_button and read_button(button) == 0:
                shared_obj.debounce_button = False
                shared_obj.fsm.compute_next_state(shared_obj.ev['press button'])
        elif state == 2:
            # get time from server
            uart.write(b'G')
            while uart.any() == 0:
                continue
            dt = uart.read(19).decode()
            time = dt.split()[1].split(':')
            print(time)
            shared_obj.digital_clock.set_time(int(time[0]), int(time[1]), int(time[2]))
            shared_obj.fsm.compute_next_state(shared_obj.ev['unconditional'])
        else:
            print('Are you OK, Annie?')
            break