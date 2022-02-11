<h1 align="center">
  Rudder
</h1>

<h3 align="center">
   Reverse Engineering the Tiller Time Tracker
</h3>

## What is Tiller?

https://user-images.githubusercontent.com/10828202/153549476-6c20644d-f848-43ba-a5b3-49c0e4534888.mp4


## Why?

Because the hardware is top-notch, and I want to reuse it! I mean just check out this:

> **Machined aluminium** - A precision machined aluminium dial perfectly meets your finger, giving a delightful tactility to using Tiller.
>
> **Precision bearing** - Tiller uses a perfectly smooth rotary bearing, engineered to provide a satisfying resistance navigating between tasks.
>
> **Reliable USB** - Tiller uses a hardwired connection to your computer, meaning always-on reliability and no batteries to charge.
>
> **Perfectly weighted** - Tiller's weight, combined with its rubber pad, means that it stays put on your desk, right where you need it.

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
