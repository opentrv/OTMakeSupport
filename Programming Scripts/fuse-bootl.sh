#!/bin/sh

sudo /home/mark/m/dev/arduino/arduino-1.6.5-r5/hardware/tools/avr/bin/avrdude -C/home/mark/m/dev/arduino/arduino-1.6.5-r5/hardware/tools/avr/etc/avrdude.conf  -patmega328p -c usbtiny -e -Ulock:w:0x3F:m -Uefuse:w:0x06:m -Uhfuse:w:0xde:m -Ulfuse:w:0x42:m 

#sudo /usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf
sudo /home/mark/m/dev/arduino/arduino-1.6.5-r5/hardware/tools/avr/bin/avrdude -C/home/mark/m/dev/arduino/arduino-1.6.5-r5/hardware/tools/avr/etc/avrdude.conf  -patmega328p -c usbtiny -Uflash:w:/home/mark/m/dev/arduino/arduino-1.6.5-r5/hardware/arduino/avr/bootloaders/atmega/atmega328_1b.hex:i -Ulock:w:0x2F:m 

###sudo /usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf  -patmega328p -cusbtiny -Uflash:w:V0p2_Main.cpp.hex:i

###/tmp/build932008652072839607.tmp/V0p2_Main.cpp.hex
