# Hardware testing rig for V0p2 REV7/DORM1/TRV1
## Aim
- Test the hardware on the REV7.
- Run on the Raspberry Pi.
- Load program on the REV7, plug it in and hit go.

## Todo List
- [ ] Serial Setup.
- [ ] Device Auto Detection.
- [x] Serial Parsing.
- [x] Generic test function.
- [x] List of Expected Results.
- [ ] Specific Tests.
- [ ] Flashing the firmware.
- [ ] Relay Board Control.

## Requirements
- Python 3.4 (possibly 3.5).
- Rapsberry Pi.
- FTDI cable.
- FTDI to I2CEXT14 adaptor.
- Relay board.

## Program Flow
- Start and init program
    - Start a serial connection.
- Device plugged in to serial.
    - Device switches on and sends a default string.
    - Pi sees string.
        - Create an array to store results.
- Tests:
    1. UILED
    2. Supply
    3. XTal
    4. Light Sensor
    5. SHT21
    6. RFM23B
    7. Buttons
    8. Potentiometer
    9. MotorLeft
    10. MotorRight
- Write results to CSV
- Exit success/fail.

## Result format
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

## Notes
- I think this will automatically run when a device is plugged in.

## Appendix A: Example output when all tests passed (20160704)

REV7 Hardware Tests
Setting up Peripherals... done
Setting up I2C... done
Waiting for Xtal to settle


Testing START
Testing UILED... CHECK
Testing Supply... CHECK 300cV
Testing Xtal... PASS
Testing LightSensor... PASS 29
Testing SHT21... PASS 417
Testing RFM23B... PASS
Testing Buttons... PASS
Testing Potentiometer... PASS 184
Testing MotorLeft... CHECK
Testing MotorRight... CHECK
Testing DONE