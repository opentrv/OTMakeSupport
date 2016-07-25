EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:rev7_hbridge_tester-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "REV7 H-bridge Tester"
Date "2016-07-08"
Rev ""
Comp "OpenTRV"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_02X20 P?
U 1 1 577F88DF
P 2750 4050
F 0 "P?" H 2750 5100 50  0000 C CNN
F 1 "Raspberry Pi 40 pin GPIO" V 2750 4050 50  0000 C CNN
F 2 "" H 2750 3100 50  0000 C CNN
F 3 "" H 2750 3100 50  0000 C CNN
	1    2750 4050
	1    0    0    -1  
$EndComp
$Comp
L LTV-827 U?
U 1 1 577F8941
P 8000 2400
F 0 "U?" H 7800 2800 50  0000 L CNN
F 1 "LTV-827" H 8000 2800 50  0000 L CNN
F 2 "DIP-8" H 7800 2050 50  0000 L CIN
F 3 "" H 8000 2300 50  0000 L CNN
	1    8000 2400
	-1   0    0    -1  
$EndComp
Text Notes 7700 1850 0    60   ~ 0
pin out same as\nLTV-826
Wire Wire Line
	8350 2400 8300 2400
Wire Wire Line
	8350 2300 8350 2400
Wire Wire Line
	8350 2300 8300 2300
$Comp
L R R?
U 1 1 577F89B3
P 8750 2350
F 0 "R?" V 8830 2350 50  0000 C CNN
F 1 "1K" V 8750 2350 50  0000 C CNN
F 2 "" V 8680 2350 50  0000 C CNN
F 3 "" H 8750 2350 50  0000 C CNN
	1    8750 2350
	0    1    1    0   
$EndComp
Wire Wire Line
	8300 2100 8450 2100
Wire Wire Line
	8450 2600 8300 2600
Wire Wire Line
	8450 2100 8450 2600
Wire Wire Line
	8350 2350 8600 2350
Connection ~ 8350 2350
$Comp
L CONN_01X02 P?
U 1 1 577F8B33
P 9450 2300
F 0 "P?" H 9450 2450 50  0000 C CNN
F 1 "REV7 H-bridge" V 9550 2300 50  0000 C CNN
F 2 "" H 9450 2300 50  0000 C CNN
F 3 "" H 9450 2300 50  0000 C CNN
	1    9450 2300
	1    0    0    -1  
$EndComp
Wire Wire Line
	9250 2350 8900 2350
Wire Wire Line
	9250 2250 8450 2250
Connection ~ 8450 2250
$Comp
L +3V3 #PWR?
U 1 1 577F8BCC
P 7200 1550
F 0 "#PWR?" H 7200 1400 50  0001 C CNN
F 1 "+3V3" H 7200 1690 50  0000 C CNN
F 2 "" H 7200 1550 50  0000 C CNN
F 3 "" H 7200 1550 50  0000 C CNN
	1    7200 1550
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 577F8BE8
P 7600 2750
F 0 "#PWR?" H 7600 2500 50  0001 C CNN
F 1 "GND" H 7600 2600 50  0000 C CNN
F 2 "" H 7600 2750 50  0000 C CNN
F 3 "" H 7600 2750 50  0000 C CNN
	1    7600 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7700 2300 7600 2300
Wire Wire Line
	7600 2300 7600 2750
Wire Wire Line
	7700 2600 7600 2600
Connection ~ 7600 2600
$Comp
L R R?
U 1 1 577F8C36
P 7200 1750
F 0 "R?" V 7280 1750 50  0000 C CNN
F 1 "10K" V 7200 1750 50  0000 C CNN
F 2 "" V 7130 1750 50  0000 C CNN
F 3 "" H 7200 1750 50  0000 C CNN
	1    7200 1750
	1    0    0    -1  
$EndComp
$Comp
L +3V3 #PWR?
U 1 1 577F8CF6
P 7450 1550
F 0 "#PWR?" H 7450 1400 50  0001 C CNN
F 1 "+3V3" H 7450 1690 50  0000 C CNN
F 2 "" H 7450 1550 50  0000 C CNN
F 3 "" H 7450 1550 50  0000 C CNN
	1    7450 1550
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 577F8CFC
P 7450 1750
F 0 "R?" V 7530 1750 50  0000 C CNN
F 1 "10K" V 7450 1750 50  0000 C CNN
F 2 "" V 7380 1750 50  0000 C CNN
F 3 "" H 7450 1750 50  0000 C CNN
	1    7450 1750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7450 1900 7450 2100
Wire Wire Line
	6850 2100 7700 2100
Wire Wire Line
	7200 1900 7200 2400
Wire Wire Line
	6850 2400 7700 2400
Connection ~ 7450 2100
Connection ~ 7200 2400
Wire Wire Line
	7200 1600 7200 1550
Wire Wire Line
	7450 1600 7450 1550
Text Label 6300 2100 0    60   ~ 0
out1
Text Label 6250 2400 0    60   ~ 0
out2
$Comp
L LTV-814 U?
U 1 1 577F8EFB
P 7450 5200
F 0 "U?" H 7250 5400 50  0000 L CNN
F 1 "LTV-814" H 7450 5400 50  0000 L CNN
F 2 "DIP-4" H 7250 5000 50  0000 L CIN
F 3 "" H 7475 5200 50  0000 L CNN
	1    7450 5200
	-1   0    0    -1  
$EndComp
Text Notes 7300 5950 0    60   ~ 0
recommend something\nlike this next time\ndepending on cost
$Comp
L R R?
U 1 1 577F9076
P 8000 5300
F 0 "R?" V 8080 5300 50  0000 C CNN
F 1 "1K" V 8000 5300 50  0000 C CNN
F 2 "" V 7930 5300 50  0000 C CNN
F 3 "" H 8000 5300 50  0000 C CNN
	1    8000 5300
	0    1    1    0   
$EndComp
$Comp
L CONN_01X02 P?
U 1 1 577F907C
P 8750 5150
F 0 "P?" H 8750 5300 50  0000 C CNN
F 1 "REV7 H-bridge" V 8850 5150 50  0000 C CNN
F 2 "" H 8750 5150 50  0000 C CNN
F 3 "" H 8750 5150 50  0000 C CNN
	1    8750 5150
	1    0    0    -1  
$EndComp
Wire Wire Line
	8550 5100 7750 5100
Wire Wire Line
	7750 5300 7850 5300
Wire Wire Line
	8150 5300 8550 5300
Wire Wire Line
	8550 5300 8550 5200
$Comp
L +3V3 #PWR?
U 1 1 577F934A
P 6950 4650
F 0 "#PWR?" H 6950 4500 50  0001 C CNN
F 1 "+3V3" H 6950 4790 50  0000 C CNN
F 2 "" H 6950 4650 50  0000 C CNN
F 3 "" H 6950 4650 50  0000 C CNN
	1    6950 4650
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 577F9350
P 6950 4850
F 0 "R?" V 7030 4850 50  0000 C CNN
F 1 "10K" V 6950 4850 50  0000 C CNN
F 2 "" V 6880 4850 50  0000 C CNN
F 3 "" H 6950 4850 50  0000 C CNN
	1    6950 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	6950 5000 6950 5100
Wire Wire Line
	6950 4700 6950 4650
Wire Wire Line
	6800 5100 7150 5100
$Comp
L GND #PWR?
U 1 1 577F942B
P 6950 5400
F 0 "#PWR?" H 6950 5150 50  0001 C CNN
F 1 "GND" H 6950 5250 50  0000 C CNN
F 2 "" H 6950 5400 50  0000 C CNN
F 3 "" H 6950 5400 50  0000 C CNN
	1    6950 5400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6950 5300 6950 5400
Wire Wire Line
	7150 5300 6950 5300
Text Label 6250 5100 0    60   ~ 0
out1
Connection ~ 6950 5100
Text Notes 7150 4850 0    60   ~ 0
AC opto means we only need 1 out.\nDirection is sent over serial anyway.
$Comp
L +3V3 #PWR?
U 1 1 577F96CB
P 2400 3000
F 0 "#PWR?" H 2400 2850 50  0001 C CNN
F 1 "+3V3" H 2400 3140 50  0000 C CNN
F 2 "" H 2400 3000 50  0000 C CNN
F 3 "" H 2400 3000 50  0000 C CNN
	1    2400 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	2400 3000 2400 3100
Wire Wire Line
	2400 3100 2500 3100
Wire Wire Line
	2500 3200 2100 3200
Wire Wire Line
	2500 3300 2100 3300
Wire Wire Line
	3000 3300 3150 3300
Wire Wire Line
	3150 3300 3150 3400
$Comp
L GND #PWR?
U 1 1 577F9831
P 3150 3400
F 0 "#PWR?" H 3150 3150 50  0001 C CNN
F 1 "GND" H 3150 3250 50  0000 C CNN
F 2 "" H 3150 3400 50  0000 C CNN
F 3 "" H 3150 3400 50  0000 C CNN
	1    3150 3400
	1    0    0    -1  
$EndComp
Text Label 2100 3200 0    60   ~ 0
out1
Text Label 2100 3300 0    60   ~ 0
out2
Text Notes 7700 3200 0    60   ~ 0
Current design
Text Notes 1350 2700 0    60   ~ 0
I used these pins because they're easy to find and close together.\nAny other GPIO and 3V3/GND pins can be used as long as the\npython script is modified appropriately.
Text Notes 5600 2300 0    60   ~ 0
Outputs are pulled\nlow on signal.
$Comp
L R R?
U 1 1 577FB44C
P 6700 2100
F 0 "R?" V 6780 2100 50  0000 C CNN
F 1 "1K" V 6700 2100 50  0000 C CNN
F 2 "" V 6630 2100 50  0000 C CNN
F 3 "" H 6700 2100 50  0000 C CNN
	1    6700 2100
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 577FB49F
P 6700 2400
F 0 "R?" V 6780 2400 50  0000 C CNN
F 1 "1K" V 6700 2400 50  0000 C CNN
F 2 "" V 6630 2400 50  0000 C CNN
F 3 "" H 6700 2400 50  0000 C CNN
	1    6700 2400
	0    1    1    0   
$EndComp
$Comp
L R R?
U 1 1 577FB60C
P 6650 5100
F 0 "R?" V 6730 5100 50  0000 C CNN
F 1 "1K" V 6650 5100 50  0000 C CNN
F 2 "" V 6580 5100 50  0000 C CNN
F 3 "" H 6650 5100 50  0000 C CNN
	1    6650 5100
	0    1    1    0   
$EndComp
Wire Wire Line
	6500 5100 6250 5100
Wire Wire Line
	6300 2100 6550 2100
Wire Wire Line
	6550 2400 6250 2400
$EndSCHEMATC
