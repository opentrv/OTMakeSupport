"""Script for automatically testing the REV7 hardware.

MAKE SURE THE REV7S TO BE TESTED ARE PRE-LOADED WITH THE TEST CODE FROM:
TODO put url here!

How to use:
1. Plug H-bridge tester into GPIO:
    - 3.3V -> GPIO pin 1.
    - GND  -> GPIO pin 6.
    - Others -> GPIO pins 3 & 5.
2. Plug in FTDI cable with I2CEXT adaptor attached.
3. Power up Pi.
4. Navigate to where you want the output file and run the script using:
    "python3 <path to script>/rev7HardwareTest.py>"
5. Plug the REV7 in.
    - FIRST! Plug in H-bridge adaptor to H-bridge pins.
    - Then plug in I2CEXT connector
    - Wait for LED to start blinking.
    - The script will print "ALL TESTS PASSED!" in green or "TESTS FAILED!" in red, followed by in list of failed tests.
6. Bin the REV7 according to the result and plug in the next one.
"""
import os
import serial
import time
# import traceback

# Import GPIO and do set up.
try:
    import RPi.GPIO as GPIO
    MOTOR_PINS = {'LEFT': 3, 'RIGHT': 5}  # dict to store motor test pins.
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOTOR_PINS['LEFT'], GPIO.IN)
    GPIO.setup(MOTOR_PINS['RIGHT'], GPIO.IN)
except ImportError:
    print("RPi.GPIO not found. Using null test for motor.")
    GPIO = None

# Constants
OUTPUT_FILE = os.path.realpath('/home/pi/dev/hw_test/output.txt')
SERIAL_DEV  = '/dev/ttyUSB0'
SERIAL_BAUD = 4800


class AvailableTests:
    """Implementations of REV7 hardware tests."""
    def __init__(self):
        """Init function."""
        self.voltage = 300  # Set supply voltage here.

    def pass_fail(self, result):
        """Check if the string returned is PASS or FAIL

        :param result: String with the values PASS or FAIL
        :return: 1 on 'PASS', 0 on 'FAIL' and None for any invalid input.
        """
        if result == 'PASS':
            return 1
        if result == 'FAIL':
            return 0
        else:
            return None

    def supply(self, voltage):
        """
        Check the supply voltage is within bounds.
        The value is in the init routine for now.
        :param voltage: Supply voltage in cV
        :return: 1 if within bounds, else 0.
        """
        if (voltage > self.voltage * 0.9) and (voltage < self.voltage * 1.1):  # TODO make sure bounds are ok.
            return 1
        else:
            return 0

    def serial(self, dev):
        """Test to make sure serial Rx and Tx both work.

        A loop back test checking the response.
        :param dev: The serial device to use.
        :return: 1 on pass, 0 on fail.
        """
        test_string = b'PING!'  # This is the buffer that is sent.
        dev.write(test_string)
        response = dev.readline()
        if response[:5] == test_string:  # The last two characters are \r\n
            return 1
        else:
            return 0

    def led_flashing(self):
        """Accept user input to determine if LED works.

        User input does not work properly (blocks with no timeout, requires an enter after 'any key' as well.)
        :return: 1 on pass, 0 on fail.
        """
        if input("Press Enter if LED flashing. Otherwise, press any key...") == '':
            return 1
        else:
            return 0

    def motor(self, direction):
        """Check the motor is working.

        Check either GPIO pin connected to an opto-isolator is pulled low.
        :param direction: Ignored. TODO: Fix this, or remove..
        :return: 1 on pass, 0 on fail, None if test is skipped.
        """
        try:
            # Read pins
            for i in range(10):
                if not GPIO.input(MOTOR_PINS['LEFT']):
                    return 1
                if not GPIO.input(MOTOR_PINS['RIGHT']):
                    return 1
                time.sleep(0.100)
            else:
                return 0
        except: # AttributeError:
            # Not on the RPi.
            print("Skipping Motor Test")
            return None

    def dummy(self):
        """Return None.

        :return: None to indicate no test is run.
        """
        return None

# create test class and make a dispatch table.
available_tests = AvailableTests()
TESTS = {"UILED":           available_tests.dummy,  # This will be checked by the user
         "Vcc":             available_tests.supply,  # Ignored or set to 3.3 V?
         "Xtal":            available_tests.pass_fail,
         "LightSensor":     available_tests.pass_fail,
         "SHT21":           available_tests.pass_fail,
         "RFM23B":          available_tests.pass_fail,
         "Buttons":         available_tests.pass_fail,
         "Potentiometer":   available_tests.pass_fail,
         "MotorLeft":       available_tests.motor,  # This is checked by the optoisolator
         "MotorRight":      available_tests.motor,
         "Serial":          available_tests.serial}  # This will need some thought.


class DoTest:
    """Append valid tests and results to a dictionary."""

    def __init__(self, tests, dev):
        """Init DoTest

        :param tests: Dictionary of test names and test functions.
        :param dev: Serial device.
        """
        self.tests = tests
        self.dev = dev
        self.first_token = 'Testing'
        self.results = {}
        self.n_devices_tested = 0
        self.n_devices_passed = 0
        self.n_devices_failed = 0

    def do(self, input_string):
        """Take an input string, parse, check the result and log it.

        The input string must be in the form:
            "Testing <TEST> <RESULT>( <OTHER>)\n"
        where:
            TEST: Name of test.
            RESULT: The result. Can be "PASS", "FAIL", "CHECK", "NOT IMPLEMENTED".
            OTHER: An optional sensor value.
        :param input_string: A string to process.
        :return: False if tests are not finished, True if tests finished.
        """
        result_list = self.parse(input_string)
        ret_val = self.test(result_list)
        if ret_val is True:  # TODO sort these out!
            return False
        elif ret_val is None:
            return False
        elif ret_val is False:
            self.log_result(self.results)
            return self.results

    def parse(self, input_string):
        """Parse input string.

        Check that the input starts with "Testing" and split the rest of the string.
        :param input_string:  A string to parse.
        :return: A list of strings.
        """
        try:
            input_string = input_string.split()  # split at spaces
            if input_string[0] == "Testing":  # Make sure it is a test.
                return input_string[1:]
        except:
            #print(traceback.format_exc())
            return None

    def test(self, var):
        """Run the tests.

        Calls a function from the appropriate entry of the test dictionary.
        :param var: List of strings parsed by self.parse.
        :return: TODO change these
        """
        try:
            if var[0] in TESTS:
                # This is the case where the REV7 cannot test itself.
                if var[0] == 'Serial':
                    self.results[var[0]] = TESTS[var[0]](self.dev)
                elif var[0] == 'Vcc':  # len(var) == 3:
                    self.results[var[0]] = TESTS[var[0]](int(var[2]))
                elif var[0] == 'UILED':
                    self.results[var[0]] = TESTS[var[0]]()
                elif var[0] == 'MotorLeft':
                    self.results[var[0]] = TESTS[var[0]]('LEFT')
                elif var[0] == 'MotorRight':
                    self.results[var[0]] = TESTS[var[0]]('RIGHT')
                else:
                    self.results[var[0]] = TESTS[var[0]](var[1])
                return True
            elif var[0] == 'START':
                print("Device found. Running tests...")
                self.results = {}
                self.n_devices_tested += 1
            elif var[0] == 'DONE':
                failed_tests = [x for x in self.results if self.results[x] == 0]
                if len(failed_tests) == 0:
                    self.n_devices_passed += 1
                    print("\033[92m" + "ALL TESTS PASSED!" + '\033[0m')
                else:
                    self.n_devices_failed += 1
                    print('\033[91m' + str(len(failed_tests)) + " TESTS FAILED!")
                    [print('\t' + x) for x in failed_tests]
                    print('\033[0m')
                print("Tested: " + str(self.n_devices_tested) + ',\t', end=' ')
                print("Passes: " + str(self.n_devices_passed) + ',\t', end=' ')
                print("Fails: " + str(self.n_devices_failed) + '.')
                return False
            else:
                print('\033[91m' + "Unsupported Test: " + var[0] + '\033[0m')
        except:
            #print(traceback.format_exc())
            return None

    def log_result(self, result):
        """Write out the results as a JSON string.

        :param result: Dict containing results.
        :return: None
        """
        try:
            with open(OUTPUT_FILE, 'a') as outfile:
                result = repr(result) + '\n'
                outfile.write(result)
        except:
            #print(traceback.format_exc())
            print("Could not log!")

# The actual program.
try:
    print("\n\nInitialising serial device " + SERIAL_DEV + " to " + str(SERIAL_BAUD) + ".")
    with serial.Serial(SERIAL_DEV, SERIAL_BAUD, timeout=1) as ser:  # Open serial port.
        do_test = DoTest(TESTS, ser)  # Make an instance of DoTest
        print("Waiting for device...")
        while True:
            string = ser.readline().decode()
            if len(string) > 3:
                do_test.do(string)
finally:
    try:
        print("\nCleaning up GPIO")
        GPIO.cleanup()
    except:
        pass
    print("Exiting")
