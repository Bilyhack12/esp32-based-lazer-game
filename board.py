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
buzzer = PWM(Pin(5))
ble = bluetooth.BLE()
bt = BLESimplePeripheral(ble, "Laser V1")
timer = Timer(0)

listen_to_shoot = False

def stopListeningToShoot():
    global listen_to_shoot
    listen_to_shoot = False

def startListeningToShoot():
    global listen_to_shoot
    listen_to_shoot = True

def on_receive(v):
    print("RX", v)
    if(v=="shoot" and not listen_to_shoot):
        startListeningToShoot()
        
    if(bt.is_connected()):
        bt.send(v+"|"+"ok")

bt.on_write(on_receive)


while True:
    # read a value from the LDR
    value = ldr.value()
    if(value<1):
        buzzer = PWM(Pin(5))
        buzzer.freq(512)
        buzzer.duty(1022)
    else:
        buzzer.deinit()
        
    print('value = {}'.format(value))

    # a little delay
    time.sleep(0.05)

# i = 0
# while True:
#     if bt.is_connected():
#         # Short burst of queued notifications.
#         for _ in range(3):
#             data = str(i) + "_"
#             print("TX", data)
#             bt.send(data)
#             i += 1
#     time.sleep_ms(100)


