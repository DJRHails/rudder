from collections import namedtuple
import struct
import usb.core
import usb.util
import time
from pprint import pprint

VENDOR_ID = 0x16d0
PRODUCT_ID = 0x0de0

print(f"Looking for Tiller {VENDOR_ID}:{PRODUCT_ID}")

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError("device not found")

# dev.set_configuration()

cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]


if dev.is_kernel_driver_active(intf.bInterfaceNumber):
    dev.detach_kernel_driver(intf.bInterfaceNumber)
    usb.util.claim_interface(dev, intf.bInterfaceNumber)

def is_out_endpoint(e):
    return usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT

def is_in_endpoint(e):
    return usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN


ep_out = usb.util.find_descriptor(
    intf,
    custom_match=is_out_endpoint
)

ep_in = usb.util.find_descriptor(
    intf,
    custom_match=is_in_endpoint
)

# 01 - pressed (?) 
# FF - radial velocity (b) -5 to +5 for normal motion, never gets close to midpoint at usable speeds.
# F6 - unknown/led_state (x) - 2nd least significant bit, 1101 = LED ON, 1111 = LED OFF 
# 13 - unknown (x)
# c4 - unknown (x)
# 0c - unknown (x)
# 78 - pressure (B)
# 40 - unknown (x)
# 18 - unknown (x)
# 00 - unknown (x)
PACKET_FORMAT = "?bxxxxBxxx"
RECORD_SIZE = 8
BATCH_SIZE = 1
TillerState = namedtuple('TillerState', ['pressed', 'velocity', 'pressure'])

def parse(record) -> TillerState:
    unpacked = struct.unpack(PACKET_FORMAT, record)
    return TillerState._make(unpacked)

def is_steady_state(state: TillerState):
    for r in state._asdict().values():
        if r:
            return False
    
    return True

def chunk(batched, chunk_size):
    for i in range(0, len(batched), chunk_size):
        yield batched[i:i + chunk_size]

def turn_led_on():
    ep_out.write('0x3001')

def turn_led_off():
    ep_out.write('0x3000')

record_count = 0
led_state = 0

while(True):
    dat = ep_in.read(10 * BATCH_SIZE)
    
    print(bytearray(dat[:10]).hex(' ', 1))
    turn_led_on()
    for c in chunk(dat, 10):
        state = parse(c)
        if not is_steady_state(state):
            print(state)

    # record_count += 1

    # if not record_count % 100:
    #     print(f"Flipping @ {record_count}")
    #     if led_state:
    #         turn_led_off()
    #         led_state = 0
    #     else:
    #         turn_led_on()
    #         led_state = 1

    # ep_out.write(0x3000)
