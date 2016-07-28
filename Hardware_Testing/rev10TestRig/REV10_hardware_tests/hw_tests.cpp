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
#define CONFIG_REV10_SECURE_BHR // Basic config for REV7
#include <OTV0p2_CONFIG_REV10.h> // the actual config
#include <OTV0p2Base.h>
#include <OTV0p2_Board_IO_Config.h>
#include <OTRadioLink.h>
#include <OTRFM23BLink.h>
#include "Wire.h"
#include "hw_tests.h"


OTV0P2BASE::OTSoftSerial2<SOFTSERIAL_RX_PIN, SOFTSERIAL_TX_PIN, 9600> sim900; // 9600 is the serial baud

OTV0P2BASE::RoomTemperatureC16_TMP112 temp;
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
 * @brief   Tests TMP112
 * @note    Test passes if given a reasonable value (between 15 and 40 C)
 * @todo    Humidity test?
 */
void testTMP112()
{
    uint16_t val;
    Serial.print(F("Testing TMP112 "));
    Serial.flush();
    val = temp.read();
    if( (val > (15*16)) && (val < (40*16))) Serial.print(F("PASS "));
    else Serial.print(F("FAIL ")); 
//    Serial.print(sht21Humidity.read());
//    Serial.println("% ");
    Serial.println(val);
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
 * @brief   Starts flashing the LED.
 * @note    Call this first?
 */
void testLEDs()
{ 
    Serial.print(F("Testing UILED "));
    pinMode(LED_HEATCALL_L, OUTPUT); // make sure set to output
    pinMode(OUT_HEATCALL, OUTPUT); // make sure set to output
    Serial.println(F("CHECK"));
    Serial.println(F("Testing DONE"));
    while(1) {
        digitalWrite(LED_HEATCALL_L, LOW);
        digitalWrite(OUT_HEATCALL, LOW);
        delay(100);
        digitalWrite(LED_HEATCALL_L, HIGH);
        digitalWrite(OUT_HEATCALL, HIGH);
        delay(500);
    }
    Serial.flush();
}


/**
 * @brief   Starts flashing the LED.
 * @note    Call this first?
 */
void testHeatCall()
{ 
    Serial.print(F("Testing HeatCall "));
    pinMode(OUT_HEATCALL, OUTPUT); // make sure set to output
    Serial.println(F("CHECK"));
    digitalWrite(OUT_HEATCALL, LOW);
    delay(100);
    digitalWrite(OUT_HEATCALL, HIGH);
    Serial.flush();
}


/**
 * @brief   Test SIM900 present.
 */
void testSIM900()
{
    char buf[9];
    const char mystring[] = "AT";
    memset(buf, 0, sizeof(buf));
    Serial.print(F("Testing SIM900 "));
    pinMode(REGULATOR_POWERUP, OUTPUT);
    pinMode(A2, OUTPUT);
    sim900.begin(0);
    digitalWrite(REGULATOR_POWERUP, LOW);
    digitalWrite(A2, LOW);
    delay(500);
    digitalWrite(A2, HIGH); // make sure it's turned on.
    delay(1000);
    digitalWrite(A2, LOW);
    delay(2000);
    

    sim900.println(mystring);
    for(uint8_t i = 0; i < sizeof(buf); i++){
        buf[i] = sim900.read();
    }
    if(!strncmp(buf, mystring, 2)) Serial.println(F("PASS"));
    else Serial.println(F("FAIL"));
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

