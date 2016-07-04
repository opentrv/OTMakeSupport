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
 * A set of hardware tests for V0p2 devices.
 * Explanation:
 * Tests return a string in the form "Testing <TEST>... <RESULT>( <OTHER>)\n"
 * Where:
 *    - TEST:   The peripheral being tested.
 *    - RESULT: The result. Can be "PASS", "FAIL", "CHECK" or "NOT IMPLEMENTED"
 *    - OTHER:  Optionally, the test can return additional information (such as sensor data).
 */

#ifndef HW_TESTS_H
#define HW_TESTS_H

/************************************** Setup Functions ******************************/
 
 
/**
 * @brief   Sets up TOSC registers for asyncronous capture to Timer X
 * @note    powerSetup() disables everything and then enables@
 *          - Timer 0 (arduino functions)
 *          - Timer 2 (xtal capture timer)
 */
void setupBasicPeripherals();
 
/**
 * @brief   Sets up I2C bus
 */
void setupI2C();
 
/**
 * @brief   Sets up pins that are not defined by other peripheral setup
 *          - Set RN2483 ~reset to high (non reset state)
 *          - Power up photodiode/any "intermittent peripherals"
 *          - Enable boost reg to power up QM-1
 */
void setupPins();

void setupRFM23B();

/**
 * @brief   Sets up software serial on relevant pins
 */
void setupSoftSerial();

/************************************** Test Functions ******************************/
 
/**
 * @brief   Tests supply voltage against internal reference
 * @todo    Implement test
 */
void testVcc();
 
/**
 * @brief   Tests xtal against internal high speed RC oscillator
 */
void testXtal();

/**
 * @brief   Tests light sensor. Prints failed if value is 0 or 255, else prints value.
 */
void testLightSensor();

/**
 * @brief   Tests I2C device at address for ACK
 * @retval  0 success
 *          1 buffer error (should never happen)
 *          2 NACK received
 *          3 NACK received
 *          4 other error
 */
uint8_t testI2CDev(uint8_t addr);

/**
 * @brief   Scans I2C bus for possible devices on the REV10 and prints to serial.
 */
void scanI2C();

/**
 * @brief   Tests SHT21
 */
void testSHT21();

/**
 * @brief   Test for response from RFM23B
 */
void testRFM23BBasic();

/**
 * @brief   Flashes LED
 */
void testUILED();

/**
 * @brief   Checks buttons are not stuck.
 */
void testButtonsUnstuck();

/**
 * @brief   Tests pot is not at either end.
 */
void testPotCentred();

/**
 * @brief   Briefly set motor drive left low.
 * @note    Actual verification performed by Raspberry Pi.
 *          Requires dual optoisolators to be connected accross motor pins.
 */
void testMotorLeft();

/**
 * @brief   Briefly set motor drive right low.
 * @note    Actual verification performed by Raspberry Pi.
 *          Requires dual optoisolators to be connected accross motor pins.
 */
void testMotorRight();


/**
 * @brief   Tests QM-1
 * @note    This requires boostRegEn_pin to be set high (+delay for QM-1 to start properly?)
 */
void testQM1();

/**
 * @brief   Tests TMP112
 */
void testTMP112();

/**
 * @brief   Tests RN2483 is present
 * @todo    get this working
 */
void testRN2483();

#endif // HW_TESTS_H
