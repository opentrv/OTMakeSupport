#!/bin/sh

# Script for programming OpenTRV V0p2 boards using a USBTiny ISP.
# 
# Notes:
# - Change ARDUINO to point to your arduino installation.
# - Change HEXFILE to the name of the file you wish to burn.
# - Run the script from the directory containing the hex file.

ARDUINO=~/openTRV/arduino-1.6.8
HEXFILE=V0p2_Main.ino.hex

sudo $ARDUINO/hardware/tools/avr/bin/avrdude -C$ARDUINO/hardware/tools/avr/etc/avrdude.conf  -patmega328p -cusbtiny -Uflash:w:$HEXFILE:i
