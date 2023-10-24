from machine import Pin, PWM, Timer
import time
import uasyncio as asyncio
import bluetooth
from ble_simple_central import BLESimpleCentral

button = Pin(23, Pin.OUT)
laser = Pin(25, Pin.OUT)
ble = bluetooth.BLE()
central = BLESimpleCentral(ble)


timer = Timer(0)

not_found = False

def on_scan(addr_type, addr, name):
    global not_found
    if addr_type is not None:
        print("Found peripheral:", addr_type, addr, name)
        central.connect()
    else:
        not_found = True
        print("No peripheral found.")

central.scan(callback=on_scan)
# Wait for connection...
while not central.is_connected():
    time.sleep_ms(100)
    if not_found:
        break

print("Connected")

def ascii_to_string(arr):
    return ''.join(chr(code) for code in arr)

def on_rx(v):
    v = ascii_to_string(v)
    print("RX", v)
    if(v.split("|")[0] == "shoot" and v.split("|")[1] == "ok"):
        shoot()

central.on_notify(on_rx)

with_response = False

can_shoot = True

def shoot():
    laser.value(1)
    time.sleep_ms(100)
    laser.value(0)

# def on_button_clicked(p):
#     global can_shoot
#     print(0)
#     if(can_shoot):
#         print(1)
#         can_shoot = False
#         #shoot
#         shoot()
#         time.sleep(2)
#         can_shoot = True
#     else:
#         print(2)


def allowShoot(value):
    global can_shoot
    can_shoot = True
    timer.deinit()

def blockShoot():
    global can_shoot
    can_shoot = False

async def waitToAllowShoot():
    global can_shoot
    can_shoot=False
    await asyncio.sleep(3)
    can_shoot = True
    
timer = Timer(0)

def sendShootRequest():
    if central.is_connected():
        central.write("shoot", False)

def main():
    global can_shoot, timer
    while True:
        button_pressed = button.value() == 1
        #print(button.value(), end=" - ")
        if(button_pressed and can_shoot):
            sendShootRequest()
            blockShoot()
            timer.init(mode=Timer.ONE_SHOT, period=500, callback=allowShoot)
#             waitTask = asyncio.create_task(waitToAllowShoot())
#             await asyncio.gather(waitTask)
        #print("go")
        time.sleep_ms(100)

main()
