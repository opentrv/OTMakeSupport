# REV10 hardware test system

## Aim
To make sure all hardware aboard REV10s is working before they get a serial number and are programmed.

## Required Equipment
### Test Equipment
- 1x Raspberry Pi w/ SD Card.
- 1x Powered USB hub.
- 1x USBTinyISP w/ USB cable.
- 2x FTDI cable.
- 2x 5 V Micro USB power supplies.
- ??x 'golden' REV10 boards.

### Stuff needed to run tests
- 3x mains plugs (can avoid this by running everything off USB hub)

### For SSH over WIFI
- WIFI dongle for Pi.
- WIFI access point.
- WIFI connected computer with ssh/putty installed.

### For SSH over Ethernet
- Ethernet cable for Pi.
- Router/switch with DHCP host.
- Computer connected to same network with ssh/putty installed.

### For using the Pi directly
- HDMI Monitor.
- Keyboard (and optionally mouse).

## Tests
- VCC
    - Checks the supply voltage from the 3.3V regulator.
    - Should be 330 cV.
- Serial
    - Performs a loop-back test on the hardware UART.
    - Sends "PING" and compares to what it receives.
- LightSensor
    - Checks that the light sensor is not measured as 0 or 255.
- RFM23B
    - Checks that the RFM23B can be talked to and it's registers set.
- TMP112
    - Checks that the TMP112 returns a sane value (i.e. between 15 and 40 C)
- SIM900
    - Checks that the SIM900 responds to an AT command.
- UILED
    - Flashes LED at the end of the tests.
- HeatCall
    - Turns the relay and LED1 on.
- PSU
    - This is not implemented as it involves mains power.
    
## Troubleshooting
- Make sure the SD Card is plugged into the Pi.
- Make sure all usb devices are plugged into a powered USB hub.
- If SIM900 test failed, is red light on the module on?
    - If not, is JP bridged? <photo>

