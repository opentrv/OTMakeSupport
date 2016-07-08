# Hardware testing rig for V0p2 REV7/DORM1/TRV1
## Aim
- Test the hardware on the REV7.
- Run on the Raspberry Pi.
- Load program on the REV7, plug it in and it runs.

## Todo List
- [x] Serial Setup.
- [x] Device Auto Detection.
- [x] Serial Parsing.
- [x] Generic test function.
- [x] List of Expected Results.
- [x] Specific Tests.
- [ ] Flashing the firmware.
- [ ] Relay Board Control.
- [x] Log results.

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
    - Pi sees string and runs tests.
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
    - Write results to file as json objects.
    - Print success (in green) or fail (in red)
- Exit with CTRL-C

## Serial Comms
The output from the REV7 is a string in the form:
```
Testing <TEST>... <RESULT>( <OTHER>)\n
```

TEST: Name of the test being run.

RESULT:  The result of the test. This can take 4 values:
- PASS:  The test has passed.
- FAIL:  The test has failed.
- CHECK: The REV7 can not check the result itself.
- NOT IMPLEMENTED: The test has not been implemented yet.

OTHER:   Optionally, the device may also return a sensor value (e.g. supply voltage, temperature etc.).

## Notes
- This will automatically run when a device is connected to serial and powered up.
- Results are logged to a file as JSON objects.
    - The key is the test name.
    - The result is 1 for a pass or 0 for a fail.

## Appendix A: Example output when all tests passed (20160704)
```
Initialising serial device /dev/ttyUSB0 to 4800.
Waiting for device...
Device found. Running tests...
ALL TESTS PASSED!
Tested: 1 Passes: 1 Fails: 0
```

## Appendix A: Example output when tests are failed. (20160704)
```
Initialising serial device /dev/ttyUSB0 to 4800.
Waiting for device...
Device found. Running tests...
TESTS FAILED!
	UILED
	MotorRight
	MotorLeft

Tested: 1,	 Passes: 0,	 Fails: 1.
```