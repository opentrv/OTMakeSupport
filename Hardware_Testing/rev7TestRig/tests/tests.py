"""
Unit tests for rev7HardwareTest.py
"""

# TODO update tests!

from rev7HardwareTest import DoTest, TESTS

def test_pass_case():
    my_test = DoTest(TESTS)
    # Pass case:
    test_string = "Testing SHT21... PASS 417"
    assert my_test.parse(test_string) == ['SHT21', 'PASS', '417']
    assert my_test.do(test_string) == ['SHT21', 'PASS', '417']

def test_first_token_wrong():
    my_test = DoTest(TESTS)
    # First Token Wrong:
    test_string = "blah SHT21... PASS 417"
    assert my_test.parse(test_string) == None
    assert my_test.do(test_string) == None

def test_second_token_wrong():
    my_test = DoTest(TESTS)
    # First Token Wrong:
    test_string = "Testing blah... PASS 417"
    assert my_test.parse(test_string) == ['blah', 'PASS', '417']
    assert my_test.do(test_string) == None

def test_input_none():
    my_test = DoTest(TESTS)
    # First Token Wrong:
    test_string = None
    assert my_test.parse(test_string) == None
    assert my_test.do(test_string) == None