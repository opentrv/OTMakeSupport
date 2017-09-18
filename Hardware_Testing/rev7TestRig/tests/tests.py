# *************************************************************
#
# The OpenTRV project licenses this file to you
# under the Apache Licence, Version 2.0 (the "Licence");
# you may not use this file except in compliance
# with the Licence. You may obtain a copy of the Licence at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the Licence is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the Licence for the
# specific language governing permissions and limitations
# under the Licence.
#
# *************************************************************
# Author(s) / Copyright (s): Deniz Erbilgin 2016
#                            Damon Hart-Davis 2017


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
