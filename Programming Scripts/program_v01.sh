#!/bin/sh

# Script for programming OpenTRV V0p2 boards using a USBTiny ISP.
# 
# Notes:
# - Change ARDUINO to point to your arduino installation.
# - Change HEXFILE to the name of the file you wish to burn.
# - Run the script from the directory containing the hex file.

HEXFILE=REV10_hardware_tests.ino.hex

sudo avrdude -patmega328p -cusbtiny -Uflash:w:$HEXFILE:i

