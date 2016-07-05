"""
Script for automatically testing the REV7 hardware.
"""
import sys

# Constants
# OUTPUT_FILE = sys.path('./rev7HWTestResults.csv')
# SERIAL_DEV  = '/dev/tty/USB0'
TESTS = {"UILED": 'CHECK',  # todo This will be checked by the user
         "Supply": 'CHECK',  # Ignored or set to 3.3 V?
         "Xtal": "PASS",
         "LightSensor": "PASS",
         "SHT21": "PASS",
         "RFM23B": "PASS",
         "Buttons": "PASS",
         "Potentiometer": "PASS",
         "MotorLeft": "CHECK",  # This is checked by the optoisolator
         "MotorRight": "CHECK"}  # Same as above

class DoTest():
    """
    Appends valid tests and results to a dictionary.
    The dictionary is returned if the test is successfully completed.
    """
    def __init__(self, tests):
        """

        :param test: A dictionary containing the expected test names and pass results.
        """
        self.tests = tests
        self.first_token = 'Testing'
        self.results = {}
        self.passes = 0

    def do(self, string):
        """

        Runs a test on the string passed in.
        Expected to be in the format:
        Testing <TEST>... <RESULT>( <OTHER>)\n
        Example:
        >>> TEST_DICT = {"UILED": "CHECK", "SHT21": "PASS"}
        >>> my_test = DoTest(TEST_DICT)
        >>> my_string = "Testing SHT21... PASS 417"
        >>> my_test.do(my_string)
        ['SHT21', 'PASS', '417']
        :param result: String from the REV7
        :return: Result of test or None if incorrect format.
        """
        string = self.parse(string)
        ret_val = self.test(string)
        if ret_val is True:
            return False
        if ret_val is False:
            self.log_result(self.results)
            return self.results
        if ret_val is None:
            pass

    def parse(self, string):
        """
        Parses the test into the correct format.
        e.g.
        >>> TEST_DICT = {"UILED": "CHECK", "SHT21": "PASS"}
        >>> my_test = DoTest(TEST_DICT)
        >>> my_string = "Testing SHT21... PASS 417"
        >>> my_test.parse(my_string)
        ['SHT21', 'PASS', '417']
        :param string: String to parse.
        :return: None if wrong format, else a list of strings containing test results.
        """
        try:
            string = string.split()  # split at spaces
            if string[0] == "Testing":  # Make sure it is a test.
                return string[1:]
        except:
            return None

    def test(self, var):
        """

        :param var:
        :return: True: Test successful
        :return: False: Reached the end of tests.
        :return: None: Invalid value
        """
        if var[0] in TESTS:
            pass_fail = 0
            if var[1] == 'CHECK':
                # This is the case where the REV7 cannot test itself.
                pass
            if var[1] == 'PASS':
                pass_fail = 1
                self.passes += 1
            self.results[var[0]] = pass_fail
            return True
        if var[0] == 'START':
            self.results = {}
        if var[0] == 'DONE':
            return False
        else:
            return None

    def log_result(self, result):
        with open('/home/denzo/git/OTMakeSupport/Hardware_Testing/rev7TestRig/rev7HardwareTest/output.txt',
                  'a') as outfile:
            result = repr(result) + '\n'
            outfile.write(result)

# test stuff
do_test = DoTest(TESTS)
with open('/home/denzo/git/OTMakeSupport/Hardware_Testing/rev7TestRig/rev7HardwareTest/example_result.txt', 'r') as infile:
    for line in infile:
        if line[:4] == "Test":
            foo = do_test.do(line)
            print(foo)

