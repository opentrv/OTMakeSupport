/*
The OpenTRV project licenses this file to you
under the Apache Licence, Version 2.0 (the "Licence");
you may not use this file except in compliance
with the Licence. You may obtain a copy of the Licence at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the Licence is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the Licence for the
specific language governing permissions and limitations
under the Licence.

Author(s) / Copyright (s): Deniz Erbilgin 2016
*/

/**
 * Set of tests for REV7 hardware.
 * High Priority Tests:
 *     - [x] Supply voltage : Print measured voltage to serial
 *     - [x] Xtal           : Check resonator frequency against internal RC
 *     - [x] Phototransistor: Perform a reading and check value is sane.
 *     - [x] SHT21          : Perform a reading and check value is sane.
 *     - [?] RFM23B         : Test RFM23B responds TODO make sure this is correct
 *     - [x] LED            : Flash LED (work out specifics)
 *     - [x] Buttons        : Make sure buttons are not stuck.
 *     - [x] Potentiometer  : Perform a reading and check value is sane.
 *     - [x] H-Bridge       : TBD
 * Low Priority Tests:
 *     - [ ] RFM23B Rx/Tx   : Make sure RFM23B can Rx/Tx.
 *     - [*] Scan I2C bus   : Check what is connected to I2C.
 *     - [ ] Motor current  : Make sure we can properly measure motor current.
 *     - [ ] Pot Wiggle     : 
 *     - [ ] Button press   : Check button actually works.
 *     - [ ] EEPROM test    : ???
 *     - [ ] Shaft encoder  : Make sure it isn't doing anything?
 *     
 * @todo   
 */

#include <Wire.h>
#include "hw_tests.h"

#include <OTV0p2Base.h>



/************************ Other Constants ****************************/
// Xtal
static const uint8_t xtalExpectedValue = 122;  // Expected value from xtal
static const uint8_t xtalMaxDeviation  =   2;  // Max acceptable deviation from xtal
// SHT21
static const uint8_t sht21_i2cAddr  = 0x40; // SHT21 I2C bus address ///TODO pull in from OTV0P2Base
// RFM23B
// Pot
static const uint8_t potMaxExpectedValue = 100;
static const uint8_t potMinExpectedValue = 20;
// H-bridge

/************************ Objects and variables **********************/

void setup() {
    /**
     * 1) Put all pins in safe state (low power not as important).
     * 2) Setup Xtal first to give time to settle
     * 3) Setup ADC0
     * 4) Setup software serial
     * 5) Setup I2C
     * 6) Wait a couple of secs
     */
     
     Serial.begin(4800); // start serial connection for debug output
     Serial.println(F("\n\nREV7 Hardware Tests"));
     setupBasicPeripherals();
     setupI2C();
     setupRFM23B();
     Serial.println(F("Waiting for Xtal to settle"));
     delay(2000); // TODO can this be safely shortened?
}

void loop() {
    /**
     * 1) Test Vcc
     * 2) Test Xtal
     * 3) Test light sensor
     * 4) Test RN2483
     * 5) Scan I2C bus
     * 6) Test available I2C devices sequentially
     */
     Serial.println(F("\n\nStarting Tests..."));

     testUILED();
     testVcc();
     testXtal();
     testLightSensor();
     scanI2C();
     testSHT21();
     testRFM23BBasic();
     testButtonsUnstuck();
     testPotCentred();
     testMotorLeft();
     testMotorRight();
     delay(5000);
}


