#!/bin/sh

# *************************************************************
#
# The OpenTRV project licenses this file to you
# under the Apache Licence, Version 2.0 (the "Licence");
# you may not use this file except in compliance
# with the Licence. You may obtain a copy of the Licence at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the Licence is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Licence for the
# specific language governing permissions and limitations
# under the Licence.
#
# *************************************************************
# Author(s) / Copyright (s): Deniz Erbilgin 2016
#                            Mark Hill 2016

# Script for programming OpenTRV V0p2 boards using a USBTiny ISP.
# 
# Notes:
# - Change ARDUINO to point to your arduino installation.
# - Change HEXFILE to the name of the file you wish to burn.
# - Run the script from the directory containing the hex file.

ARDUINO=~/openTRV/arduino-1.6.8
HEXFILE=V0p2_Main.ino.hex

sudo $ARDUINO/hardware/tools/avr/bin/avrdude -C$ARDUINO/hardware/tools/avr/etc/avrdude.conf  -patmega328p -cusbtiny -Uflash:w:$HEXFILE:i
