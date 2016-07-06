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
 *
 */

#include <Arduino.h>
#define CONFIG_DORM1 // Basic config for REV7
#include <OTV0p2_CONFIG_REV7.h> // the actual config
#include <OTV0p2Base.h>
#include <OTV0p2_Board_IO_Config.h>
#include <OTRadioLink.h>
#include <OTRFM23BLink.h>
#include "Wire.h"
#include "hw_tests.h"


OTV0P2BASE::RoomTemperatureC16_SHT21 sht21Temp;
OTV0P2BASE::HumiditySensorSHT21 sht21Humidity;
OTV0P2BASE::SupplyVoltageCentiVolts Supply_cV;
OTRFM23BLink::OTRFM23BLink<PIN_SPI_nSS, -1, 1, false> RFM23B; // Do not allow Rx

/************************************** Setup Functions ******************************/

/**
 * @brief   Sets up low speed oscillator, serial and ADC peripherals.
 * @note    powerSetup() disables everything and then enables
 *          - Timer 0 (arduino functions)
 *          - Timer 2 (xtal capture timer)
 */
void setupBasicPeripherals()
{
//    Serial.print(F("Setting up Peripherals... "));
    OTV0P2BASE::IOSetup();// IO setup for safety, and to avoid pins floating.
    OTV0P2BASE::powerSetup(); // Standard V0p2 startup method.
    OTV0P2BASE::powerUpSerialIfDisabled<4800>();
    OTV0P2BASE::powerUpADCIfDisabled();
    digitalWrite(MOTOR_DRIVE_ML, HIGH);
    digitalWrite(MOTOR_DRIVE_MR, HIGH);
    pinMode(MOTOR_DRIVE_ML , OUTPUT);
    pinMode(MOTOR_DRIVE_MR , OUTPUT);
//    Serial.println(F("done"));
    Serial.flush();
}



/**
 * @brief   Sets up I2C bus
 */
void setupI2C()
{
//    Serial.print(F("Setting up I2C... "));
    OTV0P2BASE::powerUpTWIIfDisabled();
//    Serial.println(F("done"));
    Serial.flush();
}

/**
 * @brief   Sets up pins that are not defined by other peripheral setup
 *          - Power up photodiode/any "intermittent peripherals"
 * @todo    Use pin defs from OTV0p2Base
 */
void setupPins()
{
//    Serial.print(F("Setup pins... "));
//    pinMode(RN2483_Rst_pin, OUTPUT);
//    pinMode(IO_Powerup_pin, OUTPUT);
//    pinMode(BoostRegEn_pin, OUTPUT);
//    digitalWrite(RN2483_Rst_pin, HIGH);
    digitalWrite(IO_POWER_UP, HIGH); // Power up peripherals
//    digitalWrite(BoostRegEn_pin, HIGH);
//    Serial.println(F("done"));
    Serial.flush();;
}

/**
 * @brief   setup RFM23B
 */
static const uint8_t nPrimaryRadioChannels = 1;
static const OTRadioLink::OTRadioChannelConfig RFM23BConfigs[nPrimaryRadioChannels] =
{
// GFSK channel 0 full config, RX/TX, not in itself secure. (Picked a random config.)
OTRadioLink::OTRadioChannelConfig(OTRFM23BLink::StandardRegSettingsGFSK57600, true),
};
void setupRFM23B()
{
    RFM23B.preinit(NULL);
    RFM23B.configure(nPrimaryRadioChannels, RFM23BConfigs);
}

/**
 * @brief   Sets up software serial on relevant pins
 * @note    Incomplete!
 */
void setupSoftSerial()
{
    Serial.print(F("Setting up SoftSerial... "));
//    rn2483.begin(RN2483_baud);
    Serial.println(F("FUNCTION NOT IMPLEMENTED"));
    Serial.flush();
}

/************************************** Test Functions ******************************/

/**
 * @brief   Tests serial connection both ways. Blocks until timeout.
 * 
 */
void testSerial()
{
    uint16_t endTime = 0;
    uint8_t index = 5;
    Serial.print(F("Testing Serial "));
    while(Serial.available() > 0) Serial.read();
    Serial.println(F("CHECK"));
    Serial.flush();
    endTime = millis() + 2000; // timeout in 2 seconds
    while(millis() < endTime) {
//    while(1) {
        if(Serial.available() > 0) {
          Serial.print((char)Serial.read());
          if(--index == 0) {
            Serial.println();
            return;
          }
        }
    }
    Serial.println(F("TIMEOUT"));
    Serial.flush();
}

/**
 * @brief   Tests supply voltage against internal reference
 * @todo    Implement test - What is expected value etc.
 * @todo    Can this be done with OTV0p2Base lib functions?
 */
void testVcc()
{
    uint16_t value = 0;
    Serial.print(F("Testing Vcc "));
    value = Supply_cV.read();
    Serial.print(F("CHECK "));
    Serial.println(value); // print supply voltage
//    Serial.println(F("cV"));
    Serial.flush();
}

/**
 * @brief   Tests xtal against internal high speed RC oscillator
 */
 void testXtal()
 {
    Serial.print(F("Testing Xtal "));
    delay(500);
    if(::OTV0P2BASE::HWTEST::check32768HzOscExtended()) Serial.println(F("PASS"));
    else Serial.println(F("FAIL"));
    Serial.flush();
 }

/**
 * @brief   Tests light sensor. Prints failed if value is 0 or 255, else prints value.
 * @todo    Use pin defs from OTV0p2Base
 */
void testLightSensor()
{
    uint8_t value = 0;
    Serial.print(F("Testing LightSensor "));
    value = analogRead(LDR_SENSOR_AIN);
    if( (value == 0) || (value == 255) ) Serial.print(F("FAIL "));
    else Serial.print(F("PASS "));
    Serial.println(value);
    Serial.flush();
}

/**
 * @brief   Scans I2C bus for possible devices on the REV10 and prints to serial.
 */
void scanI2C()
{
//    uint8_t value = 0;
//    Serial.println(F("Scanning I2C bus:"));
//    testTMP112();
//    testSHT21();
//    testQM1();
}

/**
 * @brief   Tests SHT21
 * @note    Test passes if given a reasonable value (between 15 and 40 C)
 * @todo    Humidity test?
 */
void testSHT21()
{
    uint16_t temp;
    Serial.print(F("Testing SHT21 "));
    Serial.flush();
    temp = sht21Temp.read();
    if( (temp > (15*16)) && (temp < (40*16))) Serial.print(F("PASS "));
    else Serial.print(F("FAIL ")); 
//    Serial.print(sht21Humidity.read());
//    Serial.println("% ");
    Serial.println(temp);
    Serial.flush();
}

/**
 * @brief   Test for response from RFM23B
 */
void testRFM23BBasic()
{
    Serial.print(F("Testing RFM23B "));
    Serial.flush();
    if( RFM23B.begin()) Serial.println(F("PASS"));  // fixme I think this returns true/false depending on if can talk to radio
    else Serial.println(F("FAIL"));
    RFM23B.end();
    Serial.flush();
}

/**
 * @brief   Tests pot is not at either end.
 * @todo    More sensible values.
 */
void testPotCentred()
{
    uint8_t value = 0;
    Serial.print(F("Testing Potentiometer "));
    value = analogRead(TEMP_POT_AIN);
    if( (value == 0) || (value == 255) ) Serial.print(F("FAIL "));
    else Serial.print(F("PASS "));
    Serial.println(value);
    Serial.flush();
}

/**
 * @brief   Checks buttons are not stuck.
 * @todo    Test values properly
 */
void testButtonsUnstuck()
{
    Serial.print(F("Testing Buttons "));
    // Check buttons not stuck in the activated position.
    // All expected to return low.
//    Serial.print(fastDigitalRead(BUTTON_LEARN_L));
//    Serial.println(fastDigitalRead(BUTTON_LEARN2_L));
    if( fastDigitalRead(BUTTON_MODE_L) ) Serial.println(F("PASS"));
    else Serial.println(F("FAIL"));
    Serial.flush();
}

/**
 * @brief   Starts flashing the LED.
 * @note    Call this first?
 */
void testUILED()
{ 
    Serial.print(F("Testing UILED "));
    pinMode(LED_HEATCALL_L, OUTPUT); // make sure set to output
    Serial.println(F("CHECK"));
    Serial.println(F("Testing DONE"));
    while(1) {
        digitalWrite(LED_HEATCALL_L, LOW);
        delay(100);
        digitalWrite(LED_HEATCALL_L, HIGH);
        delay(500);
    }
    Serial.flush();
}

/**
 * @brief   Briefly set motor drive left low.
 * @note    Actual verification performed by Raspberry Pi.
 *          Requires dual optoisolators to be connected accross motor pins.
 */
void testMotorLeft()
{
    Serial.print(F("Testing MotorLeft "));
    Serial.flush();
    digitalWrite(MOTOR_DRIVE_ML, LOW);
    delay(500);
    digitalWrite(MOTOR_DRIVE_ML, HIGH);
    Serial.println(F("CHECK"));
    Serial.flush();
    delay(1000);
}

/**
 * @brief   Briefly set motor drive right low.
 * @note    Actual verification performed by Raspberry Pi.
 *          Requires dual optoisolators to be connected accross motor pins.
 */
void testMotorRight()
{
    Serial.print(F("Testing MotorRight "));
    Serial.flush();
    digitalWrite(MOTOR_DRIVE_MR, LOW);
    delay(500);
    digitalWrite(MOTOR_DRIVE_MR, HIGH);
    Serial.println(F("CHECK"));
    Serial.flush();
    delay(1000);
}




/**
 * @brief   Tests I2C device at address for ACK
 * @retval  0 success
 *          1 buffer error (should never happen)
 *          2 NACK received
 *          3 NACK received
 *          4 other error
 */
uint8_t testI2CDev(uint8_t addr)
{
    Wire.beginTransmission(addr);
    return Wire.endTransmission();
}

/**
 * @brief   Tests TMP112
 * @todo    Use address defs from OTV0p2Base
 * @todo    Perform a conversion.
 */
void testTMP112()
{
    Serial.print(F("Checking for TMP112 "));
    Serial.println(F("NOT IMPLEMENTED"));
    Serial.flush();
}

/**
 * @brief   Tests QM-1
 * @note    This requires boostRegEn_pin to be set high (+delay for QM-1 to start properly?)
 * @todo    Incomplete
 */
void testQM1()
{
    Serial.print(F("Checking for QM-1 "));
    Serial.println(F("NOT IMPLEMENTED"));
    Serial.flush();
}

/**
 * @brief   Tests RN2483 is present
 * @todo    Incomplete
 */
void testRN2483()
{
//    char buf[9];
//    memset(buf, 0, sizeof(buf));
//    buf[8] = ' ';
    Serial.println(F("Testing RN2483 "));
//    // reset RN2483
//    digitalWrite(RN2483_Rst_pin, LOW);
//    delay(100);
//    digitalWrite(RN2483_Rst_pin, HIGH);
//    delay(1000);
//    // autobaud (break+'U')
//    digitalWrite(RN2483_Tx_pin, LOW);
//    delay(10);
//    digitalWrite(RN2483_Tx_pin, HIGH);
//    rn2483.print('U');
//    delay(100);
//    // send test message and check reply
//    rn2483.print("sys get ver\r\n");
//    rn2483.read( (uint8_t *)buf, (sizeof(buf)-1) );
//    Serial.println(buf);
    Serial.println(F("NOT IMPLEMENTED"));
    Serial.flush();
}

