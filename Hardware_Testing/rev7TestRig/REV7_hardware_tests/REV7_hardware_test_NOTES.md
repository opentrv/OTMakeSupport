# REV7 Hardware Tests
This is a sketch designed to automate fault finding on the V0p2 REV7 board.

## Features to Implement
- Make LED test flash a 'tests passed' routine to indicate success.
- Use a better string to indicate the device is attached.

## Peripherals To Test
High Priority Tests:
    - [x] Serial UART    : Implicit.
    - [x] Xtal           : Check resonator frequency against internal RC
    - [x] Phototransistor: Perform a reading and check value is sane.
    - [x] SHT21          : Perform a reading and check value is sane.
    - [x] RFM23B         : Test RFM23B responds.
    - [x] UI LED         : Turns the UI LED on. This is LED_HEATCALL in the code. (This caused me some confusion - DE)
    - [x] Buttons        : Make sure buttons are not stuck.
    - [x] Potentiometer  : Perform a reading and check value is sane.
    - [x] Motor Driver   : Two tests, one for left and one for right.
Low Priority Tests:
    - [x] Supply voltage : Print measured voltage to serial
    - [ ] RFM23B Rx/Tx   : Make sure RFM23B can Rx/Tx.
    - [ ] Scan I2C bus   : Check what is connected to I2C.
    - [ ] Motor current  : Make sure we can properly measure motor current.
    - [ ] Pot Wiggle     : 
    - [ ] Button press   : Check button actually works.
    - [ ] EEPROM test    : ???
    - [ ] Shaft encoder  : Make sure it isn't doing anything?


## Output format
The output of a test is a string in the form:
```
Testing <TEST>... <RESULT>( <OTHER>)\n
```

TEST: Name of the test being run.

RESULT:  The result of the test. This can take 4 values:
- PASS:  The test has passed.
- FAIL:  The test has failed.
- CHECK: The DUT can not check the result itself.
- NOT IMPLEMENTED: The test has not been implemented yet.

OTHER:   Optionally, the device may also return a sensor value (e.g. supply voltage, temperature etc.).

## Tests that require external checking
The following tests cannot be checked by the device and will require additional equipment/procedures.
- UI LED:
    - Visually check that the LED is turned on.
    - Prompt user on raspberry pi script?
- Motor Driver:
    - Requires a load to be attached to the H-Bridge.
    - Plug into optoisolators connected to Pi.
    - Should see if we can test this with a current sensor.
- Supply voltage:
    - Ignore.

## Appendix A: Example output when all tests passed (20160704)

REV7 Hardware Tests
Setting up Peripherals... done
Setting up I2C... done
Waiting for Xtal to settle


Starting Tests...
Testing UILED... CHECK
Testing Supply... CHECK 300cV
Testing Xtal... PASS
Testing Light Sensor... PASS 29
Testing SHT21... PASS 417
Testing RFM23B... PASS
Testing Buttons... PASS
Testing Potentiometer... PASS 184
Testing MotorLeft... CHECK
Testing MotorRight... CHECK

