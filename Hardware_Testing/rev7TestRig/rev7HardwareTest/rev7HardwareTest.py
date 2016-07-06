"""
Script for automatically testing the REV7 hardware.
"""
import os, serial

# Constants
OUTPUT_FILE = os.path.realpath('./output.txt')
SERIAL_DEV  = '/dev/ttyUSB0'
SERIAL_BAUD = 4800

class AvailableTests:
    """
    A class containing the implementations of the tests.
    """
    def __init__(self):
        self.voltage = 300  # Set supply voltage here.
        pass

    def pass_fail(self, result):
        """
        Check if the string returned is PASS or FAIL
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
        if (voltage > self.voltage * 0.9) and (voltage < self.voltage * 1.1):
            return 1
        else:
            return 0

    def serial(self, dev):
        """
        Loop back test to make sure serial Rx and Tx both work.
        :param dev: The serial device to use.
        :return: 1 on pass, 0 on fail.
        """
        test_string = b'PING!'  # This is the buffer that is sent.
        dev.write(test_string)
        response = dev.readline()
        if response[:5] == test_string:
            return 1
        else:
            return 0

    def led_flashing(self):
        """
        Accepts user input to determine if LED works.
        :return: 1 on pass, 0 on fail.
        """
        if input("Press Enter if LED flashing. Otherwise, press any key...") == '':
            return 1
        else:
            return 0

    def motor(self, direction):
        """
        Checks motor is working.
        NOT YET IMPLEMENTED!
        :param direction:
        :return:
        """
        return None

    def dummy(self):
        """
        Dummy routine.
        :return: None to indicate test is disabled.
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
    """
    Appends valid tests and results to a dictionary.
    The dictionary is returned if the test is successfully completed.
    """
    def __init__(self, tests, dev):
        """
        Init DoTest.
        :param test: A dictionary containing the expected test names and pass results.
        """
        self.tests = tests
        self.dev = dev

        self.first_token = 'Testing'
        self.results = {}
        self.n_devices_tested = 0
        self.n_devices_passed = 0
        self.n_devices_failed = 0

    def do(self, input_string):
        list = self.parse(input_string)
        ret_val = self.test(list)
        if ret_val is True:
            return False
        if ret_val is False:
            self.log_result(self.results)
            return self.results
        if ret_val is None:
            pass

    def parse(self, input_string):
        try:
            input_string = input_string.split()  # split at spaces
            if input_string[0] == "Testing":  # Make sure it is a test.
                return input_string[1:]
        except:
            return None

    def test(self, var):
        try:
            if var[0] in TESTS:
                # print(var[0])  # Print name of test.
                # This is the case where the REV7 cannot test itself.
                if var[0] == 'Serial':
                    self.results[var[0]] = TESTS[var[0]](self.dev)
                if var[0] == 'Vcc':  # len(var) == 3:
                    self.results[var[0]] = TESTS[var[0]](int(var[2]))
                if var[0] == 'UILED':
                    self.results[var[0]] = TESTS[var[0]]()
                else:
                    self.results[var[0]] = TESTS[var[0]](var[1])
                # print(self.results)
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
            return None

    def log_result(self, result):
        """
        Writes out the results as a JSON string.
        :param result:
        :return: None
        """
        try:
            with open(OUTPUT_FILE, 'a') as outfile:
                result = repr(result) + '\n'
                outfile.write(result)
        except:
            print("Could not log!")

# The actual program.
print("\n\nInitialising serial device " + SERIAL_DEV + " to " + str(SERIAL_BAUD) + ".")
with serial.Serial(SERIAL_DEV, SERIAL_BAUD, timeout=1) as ser:  # Open serial port.
    do_test = DoTest(TESTS, ser)  # Make an instance of DoTest
    print("Waiting for device...")
    while True:
        string = ser.readline().decode()
        if len(string) > 3:
            do_test.do(string)