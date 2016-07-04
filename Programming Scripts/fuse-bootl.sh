#!/bin/sh

TOOLS=~/openTRV/arduino-1.6.8
BOOTLOADER=~/.arduino15/packages/opentrv/hardware/avr/0.0.4/bootloaders/atmega328_opentrv_v0p2.hex

sudo $TOOLS/hardware/tools/avr/bin/avrdude -C$TOOLS/hardware/tools/avr/etc/avrdude.conf  -patmega328p -c usbtiny -e -Ulock:w:0x3F:m -Uefuse:w:0x06:m -Uhfuse:w:0xde:m -Ulfuse:w:0x42:m 

#sudo /usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf
sudo $TOOLS/hardware/tools/avr/bin/avrdude -C$TOOLS/hardware/tools/avr/etc/avrdude.conf  -patmega328p -c usbtiny -Uflash:w:$BOOTLOADER:i -Ulock:w:0x2F:m 

###sudo /usr/share/arduino/hardware/tools/avrdude -C/usr/share/arduino/hardware/tools/avrdude.conf  -patmega328p -cusbtiny -Uflash:w:V0p2_Main.cpp.hex:i

###/tmp/build932008652072839607.tmp/V0p2_Main.cpp.hex
