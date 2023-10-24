import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from machine import ADC, Pin, PWM, Timer
import time

class LDR:
    """This class read a value from a light dependent resistor (LDR)"""

    def __init__(self, pin, min_value=0, max_value=100):
        """
        Initializes a new instance.
        :parameter pin A pin that's connected to an LDR.
        :parameter min_value A min value that can be returned by value() method.
        :parameter max_value A max value that can be returned by value() method.
        """

        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        # initialize ADC (analog to digital conversion)
        self.adc = ADC(Pin(pin))

        # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.adc.atten(ADC.ATTN_11DB)

        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        """
        Read a raw value from the LDR.
        :return A value from 0 to 4095.
        """
        return self.adc.read()

    def value(self):
        """
        Read a value from the LDR in the specified range.
        :return A value from the specified [min, max] range.
        """
        return (self.max_value - self.min_value) * self.read() / 4095


# initialize an LDR
ldr = LDR(34)
ble = bluetooth.BLE()
bt = BLESimplePeripheral(ble, "Laser V1")
timer = Timer(0)

listening_to_shoot = False

def stopListeningToShoot(v):
    global listening_to_shoot
    listening_to_shoot = False
    if(not hit):
        buzzer = PWM(Pin(5), freq=512, duty=512)
        time.sleep(0.3)
        buzzer.deinit()
    canPlayPin.value(1)

def startListeningToShoot():
    global listening_to_shoot, hit
    hit = False
    canPlayPin.value(0)
    listening_to_shoot = True
    
timer = Timer(0)

def on_receive(v):
    v= v.decode()
    print("RX", v)
    if(v=="shoot" and not listening_to_shoot):
        startListeningToShoot()
        timer.init(mode=Timer.ONE_SHOT, period=500, callback=stopListeningToShoot)
        
    if(bt.is_connected()):
        bt.send(v+"|"+"ok")

bt.on_write(on_receive)
buzzer = None
canPlayPin = Pin(13, Pin.OUT)
hitLight = Pin(18, Pin.OUT)

while not bt.is_connected():
    pass
canPlayPin.value(1)
hit = False

while True:
    value = ldr.value()
    if(value<12 and listening_to_shoot):
        hit = True
        hitLight.value(1)
        for i in range (10):
            buzzer = PWM(Pin(5), freq=512, duty=1022)
            time.sleep(0.25)
            buzzer.deinit()
        hitLight.value(0)
        canPlayPin.value(1)
    else:
        if buzzer:
            buzzer.deinit()
    time.sleep(0.05)

