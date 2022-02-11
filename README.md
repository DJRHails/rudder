# Tiller

## Installation
```
apt install libhidapi-libusb0
```

```
lsusb
lsusb -vd 16d0:0de0 > lusb-descriptors.txt
sudo dmesg | grep 'Product: Tiller' | tail -n 1

```

- HID Device (yay!)
    - 2 Interrupt endpoints
        - 0x01 EIP 1 OUT
            - 1 x 8 B
        - 0x92 EIP 2 IN
            - 1 x 10 B
- ``


## Troubleshooting

`usb.core.USBError: [Errno 13] Access denied (insufficient permissions)`

- Check user is in `plugdev` > `groups $USER`
- sudo vim /etc/udev/rules.d/10-local.rules

```
SUBSYSTEM=="usb", ATTR{idVendor}=="16d0", ATTR{idProduct}=="0de0", MODE="0666"
```

```
sudo udevadm control --reload
sudo udevadm trigger
```