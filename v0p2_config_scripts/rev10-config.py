#!/usr/bin/env python3
"""
1. Program REV10 over avrdude
2. Tell user to remove ISP cable and attach SIM900, FTDI and power
3. Wait for prompt
4. Program REV10 key and associations
"""
import RPi.GPIO as GPIO
import sys
import csv
from subprocess import call
import serial as ser
import time

PROGRAM_PATH = 'build/REV10.1.0.4.Ark.36.V0p2_Main.cpp.standard.hex'
REV10_SERIAL = '/dev/ttyUSB0'
REV10_BAUD   = '4800'
INPUT_FILE   = 'all-nodes.csv'
OUTPUT_FILE  = 'output.csv'

REV10_POWER  = 11

REV10_POST   = b'OpenTRV: board V0.2 REV10'


# power on REV7
def powerOn():
#    print("Power on REV7")
    GPIO.output(REV10_POWER, GPIO.LOW)
    call(["/home/pi/1on.sh"])
    time.sleep(3)

#power off REV7
def powerOff():
#    print("Power off REV7")
    GPIO.output(REV10_POWER, GPIO.HIGH)
    call(["/home/pi/1off.sh"])
    time.sleep(3)

def program():
    print("----------------Programming REV10")
    call(["sudo", "avrdude", "-patmega328p", "-cusbtiny", "-e", "-Ulock:w:0x3F:m", "-Uefuse:w:0x06:m", "-Uhfuse:w:0xde:m", "-Ulfuse:w:0x42:m"])
    call(["sudo", "avrdude", "-v", "-patmega328p", "-cusbtiny", "-b4800", "-D", "-Uflash:w:"+PROGRAM_PATH+":i"])

# get keys and associated nodes from a csv
def getKeysAndNodes(serNo):
    key = ''
    nodes = ['', '', '', '']
    print("----------------Getting keys for "+serNo)
    with open(INPUT_FILE, 'r', newline='') as inputfile:
        keys = csv.reader(inputfile, delimiter=',')
        for row in keys:
            if serNo in row:
                key = row[1]
                nodes[0] = row[2]
                row = next(keys)
                nodes[1] = row[2]
                row = next(keys)
                nodes[2] = row[2]
                row = next(keys)
                nodes[3] = row[2]
        return key, nodes

def openSerialPort():
    print("----------------Opening Serial Port")
    rev10 = ser.Serial(REV10_SERIAL, REV10_BAUD, timeout = 2)
    return rev10
    #rev10.readline()
    #line = rev10.readline()
    #if line.startswith(REV10_POST):
    #    return rev10
    #else:
    #    return True

# power cycle REV7
def powerCycle(dev):
    powerOff()
    time.sleep(5)
    dev.flushInput()
    powerOn()
    time.sleep(0.5)
    line1 = dev.readline()
    print ("REV10: " + str(line1))
    line2 = dev.readline()
    print ("REV10: " + str(line2))
    if line2.startswith(REV10_POST):
        print ("------------ found REV10... " + repr(line2))
        return 1
    else:
        print("*********************************REV10 not found")
        print("********* CHECK IF POWERED ! ******")
        powerOff()
        GPIO.cleanup()
        end()
        exit()

# setup REV7 power pin
def setup():
    print("-----------------Setup REV7 power pin")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(REV10_POWER, GPIO.OUT)
    GPIO.output(REV10_POWER, GPIO.HIGH)

# close and free REV7 power pin
def end():
    print("---------------------Close and free power pin")
    powerOff()
    GPIO.cleanup()

# Wait for prompt character
def sendCmd(dev, buf):
    print ("->preparing to send command: " + str(buf))
    dev.write(b'\n')
    while(dev.read() != b'>'):
        x = 0
    print ("->detected prompt")
    dev.write(buf + b'\n')
    print ("->written command: " + str(buf))

# wait for post and initial txs to finish
def waitForCLI(dev):
    counter = 0
    dev.write(b'\n')
    string = dev.readline()
    while (string != b'>\r\n') and (counter < 5):
        print("REV10: " + repr(string))
        string = dev.readline()
        dev.write(b'\n')
        counter = counter + 1

def getREV10ID(dev):
    print("---------------Getting REV10 node ID")
#//    sendCmd(dev, b'')
#    sendCmd(dev, b'I')
    counter = 20
    id_found = False
    nodeID = b''
    line1 = b''

    while (id_found == False and counter > 0):
        sendCmd(dev, b'I\n')
        string = dev.readline()
        print("REV10: " + repr(string))
        if ("ID:" in string.decode()):
            return string[4:27].decode()
            id_found = True
        if counter == 20:
            dev.write(b'I\n')
            dev.write(b'I\n')
            dev.write(b'I\n')
            while(dev.read() != b'>'):
                print (".", end='')
            dev.write(b'I\n')
        #    sendCmd(dev, b'I')
        string = dev.readline()
        print("REV10: " + repr(string))
        if ("ID:" in string.decode()):
            return string[4:27].decode()
            id_found = True
        else:
            counter = counter - 1
            if counter == 10:
                sendCmd(dev, b'I')
    if counter == 0:
        print ("----- couldn't get ID")
        end()
        exit()
    return nodeID

def setKey(dev, key):
    print("----------------Setting Key")
    sendCmd(dev, key.encode())
    print("Key= "+key)
    print(dev.readline())
    line = dev.readline()
    line = line.decode()
    print("REV10: " + line)
    if line.startswith('B set') != True:
        print("!!!!!!!!!!!!!!!!!!failed!. Exiting.")
        end()
        exit()
 
def setNodes(dev, nodes):
    print("----------------Setting Node IDs")
    sendCmd(dev, b'A *')
    print(dev.readline())
    print(dev.readline())
    for x in nodes:
        count = 4 # tries to set the node value
        node_set = False
        while count > 0 and node_set == False:
            print("--setting node ID "+x)
            sendCmd(dev, b'A '+ x.encode())
            print("REV10: " + dev.readline().decode())
            line = dev.readline()
            print("REV10: " + line.decode())
            if "Index" in line.decode():
                node_set = True
                print ("--- node set successfully")
            time.sleep(1)
            count = count - 1
        if node_set == False:
            print ("************ node set for " + x + " failed. Quit!")
            end()
            exit()
        
def writeOut(rev10_serial_number, key, rev10ID, rev7_serial_number):
    if rev7_serial_number == "0":
        return 1
    else:
        with open(OUTPUT_FILE, 'a', newline = '') as outputfile:
            outputcsv = csv.writer(outputfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            outputcsv.writerow([str(rev10_serial_number), key, rev10ID, str(int(rev7_serial_number)), str(int(rev7_serial_number)+1), str(int(rev7_serial_number)+2), str(int(rev7_serial_number)+3)])
        return 0
def keySetCorrectly(dev):
    print ("checking for !TX key message (key not set)")
    counter = 0
    string = dev.readline()
    print ("REV10: " + string.decode())
    while (counter < 10):
        print ("REV10: " + string.decode())
        if "!" in string.decode():
             return False
        string = dev.readline()
        counter = counter + 1
    return True
    
def associationsSetCorrectly(dev, nodes):
    a_command_accepted = False
    a_command_counter = 0
    
    for x in nodes:
        counter = 0
        node_found = False
        search_term = x[0:5] + " ... " + x[-2:]
        print ("------------ searching for " + search_term)
        while node_found == False and counter <= 32: # counter just needs to be tested for more than 10
            if not a_command_accepted:
                if a_command_counter == 0:
                    sendCmd(dev, b'A ?')
                a_command_counter += 1
                if a_command_counter == 5:
                    a_command_counter = 0
            line = dev.readline()
            print ("REV10: " + line.decode(), end="")
            if (search_term in line.decode()):
                print ("------------ " + x + " found")
                node_found = True
                a_command_accepted = True
            else:
                counter = counter + 1
            if counter >= 30:
                print ("------------**** " + x + " not found")
                return False
    return True
    
    

def main(argv):
    setup()
    powerOff()
    powerOn()
    serNo = argv[0]
    rev10_serial_number = argv[1]
    print (" rev10 programmer - usage: python3 rev10-config.py 7XXX 10YYY [p]")
    print (" where 7XXX is the first of four consecutive nodes; 10YYYY is the REV10 serial number")
    print (" node IDs read from " + INPUT_FILE + " and written to " + OUTPUT_FILE)
    print (" optional p will first program using ISP")
    print ("")
    rev10ID = ''
    if len(argv) > 2 and argv[2] == "p":
        print (" ***************************** ")
        print (" ***************************** ")
        print ("")
        print (" ******** PROGRAMMING ******** ")
        print ("")
        print (" ***************************** ")
        print (" ***************************** ")
        program()  ## UNCOMMENT THIS!!!!!!!!!!!!!!!!
        powerOff()
        print (" ***************************** ")
        print (" ***************************** ")
        print ("")
        print("+++ REMOVE ICSP AND ATTACH SIM900 & FTDI +++")
        print("+++ REMOVE ICSP AND ATTACH SIM900 & FTDI +++")
        print("+++ REMOVE ICSP AND ATTACH SIM900 & FTDI +++")
        print ("")
        print (" ***************************** ")
        print (" ***************************** ")
        input("Press ENTER to continue...")  ## UNCOMMENT THIS!!!!!!!!!!!!!!!!
        input("Really (double check) press ENTER to continue...")  ## UNCOMMENT THIS!!!!!!!!!!!!!!!!
    rev10 = openSerialPort()
    powerCycle(rev10)
    print("------------------Waiting for SIM900 to register. This may take some time")
    for x in range(0, 30):
         time.sleep(1)
         print (str(30-x) + ".", end="")
         sys.stdout.flush()
    print ()
    waitForCLI(rev10)
    
    rev10key, rev7nodes = getKeysAndNodes(serNo)
    print("rev10 key= ", end='')
    print(rev10key)
    print("rev7 nodes= ", end='')
    print(rev7nodes)
    
    rev10ID = getREV10ID(rev10)    
    print("------------------rev10 ID= " + str(rev10ID))
    
    setKey(rev10, rev10key)
    setNodes(rev10, rev7nodes)
    powerCycle(rev10)
    print("------------------Waiting for SIM900 to register. This may take some time")
    print("------------------Checking key set")
    for x in range(0, 20):
         time.sleep(1)
         print (str(20-x) + ".", end="")
         sys.stdout.flush()
    print ()
    
    if keySetCorrectly(rev10) == False:
        setKey(rev10, rev10key)
        #setNodes(rev10, rev7nodes)
        powerCycle(rev10)
        print("------------------Waiting for SIM900 to register. This may take some time")
        
        for x in range(0, 20):
            time.sleep(1)
            print (str(20-x) + ".", end="")
            sys.stdout.flush()
        print ()
        
        if keySetCorrectly(rev10) == False:
            print("!!!!!!!!!!!!!!!!!!!!!!! Failed to set key! Exiting.")
            end()
            exit()
    
    print ("key set correctly")
    
    if (not associationsSetCorrectly(rev10, rev7nodes)):
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!! Failed association test. Exit time")
        end()
        exit()
    
    print ("------------ associations set correctly")
        
    print ("------------ writing to output CSV file")
    writeOut(rev10_serial_number, rev10key, rev10ID, serNo)
    print ("")
    print ("--- *** +++ ^^^         ^^^ +++ *** ---")
    print ("--- *** +++ ^^^ success ^^^ +++ *** ---")
    print ("--- *** +++ ^^^         ^^^ +++ *** ---")
    print ("")
    
    end()

if __name__ == "__main__":
    main(sys.argv[1:])
