#!/bin/sh
sudo /home/mark/m/dev/arduino/arduino-1.6.5-r5/hardware/tools/avr/bin/avrdude -C/home/mark/m/dev/arduino/arduino-1.6.5-r5/hardware/tools/avr/etc/avrdude.conf  -patmega328p -c usbtiny -e -Ulock:w:0x3F:m -Uefuse:w:0x06:m -Uhfuse:w:0xde:m -Ulfuse:w:0x42:m


/home/mark/m/dev/arduino/arduino-167/arduino-1.6.7/hardware/tools/avr/bin/avrdude -C/home/mark/m/dev/arduino/arduino-167/arduino-1.6.7/hardware/tools/avr/etc/avrdude.conf -v -patmega328p -cusbtiny  -b4800 -D -Uflash:w:V0p2_Main.cpp.standard.hex:i
