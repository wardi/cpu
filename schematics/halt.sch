EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "Clock, Reset and Halt Circuit"
Date ""
Rev "1"
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L power:GND #PWR0101
U 1 1 62BEF5AE
P 1200 7400
F 0 "#PWR0101" H 1200 7150 50  0001 C CNN
F 1 "GND" H 1205 7227 50  0000 C CNN
F 2 "" H 1200 7400 50  0001 C CNN
F 3 "" H 1200 7400 50  0001 C CNN
	1    1200 7400
	1    0    0    -1  
$EndComp
Connection ~ 4550 3000
Wire Wire Line
	5800 4900 5800 2900
Wire Wire Line
	5800 2900 5950 2900
Connection ~ 5800 2900
Wire Wire Line
	4550 3000 5000 3000
Wire Wire Line
	5600 2900 5800 2900
$Comp
L Device:R_US R7
U 1 1 62D14E22
P 6250 3050
F 0 "R7" H 6182 3004 50  0000 R CNN
F 1 "220R" H 6182 3095 50  0000 R CNN
F 2 "" V 6290 3040 50  0001 C CNN
F 3 "~" H 6250 3050 50  0001 C CNN
	1    6250 3050
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D3
U 1 1 62D14E18
P 6100 2900
F 0 "D3" H 6093 2645 50  0000 C CNN
F 1 "RED LED" H 6093 2736 50  0000 C CNN
F 2 "" H 6100 2900 50  0001 C CNN
F 3 "~" H 6100 2900 50  0001 C CNN
	1    6100 2900
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 62D14E0E
P 6250 3200
F 0 "#PWR0102" H 6250 2950 50  0001 C CNN
F 1 "GND" H 6255 3027 50  0000 C CNN
F 2 "" H 6250 3200 50  0001 C CNN
F 3 "" H 6250 3200 50  0001 C CNN
	1    6250 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 2200 5000 2800
Text GLabel 5000 2200 1    50   Input ~ 0
HLT
$Comp
L 4xxx:4011 U2
U 2 1 62BDBA91
P 5300 2900
F 0 "U2" H 5300 3225 50  0000 C CNN
F 1 "4011" H 5300 3134 50  0000 C CNN
F 2 "" H 5300 2900 50  0001 C CNN
F 3 "http://www.intersil.com/content/dam/Intersil/documents/cd40/cd4011bms-12bms-23bms.pdf" H 5300 2900 50  0001 C CNN
	2    5300 2900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6250 4900 5800 4900
$Comp
L Timer:LM555 U1
U 1 1 628E98DA
P 6750 4700
F 0 "U1" H 6750 5281 50  0001 C CNN
F 1 "LM555" H 6500 5100 50  0000 C CNN
F 2 "" H 6750 4700 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm555.pdf" H 6750 4700 50  0001 C CNN
	1    6750 4700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR05
U 1 1 628EA12C
P 6750 5100
F 0 "#PWR05" H 6750 4850 50  0001 C CNN
F 1 "GND" H 6755 4927 50  0000 C CNN
F 2 "" H 6750 5100 50  0001 C CNN
F 3 "" H 6750 5100 50  0001 C CNN
	1    6750 5100
	1    0    0    -1  
$EndComp
Wire Wire Line
	6750 4250 6750 4300
Wire Wire Line
	5550 4500 6250 4500
Wire Wire Line
	7250 4500 7750 4500
$Comp
L Device:C_Small C2
U 1 1 62905952
P 6150 4700
F 0 "C2" H 6242 4746 50  0000 L CNN
F 1 "1u" H 6242 4655 50  0000 L CNN
F 2 "" H 6150 4700 50  0001 C CNN
F 3 "~" H 6150 4700 50  0001 C CNN
	1    6150 4700
	0    1    1    0   
$EndComp
Wire Wire Line
	7300 4900 7250 4900
Wire Wire Line
	7300 4700 7250 4700
Wire Wire Line
	6050 4700 6050 4250
Connection ~ 5300 4000
Connection ~ 5300 5400
Wire Wire Line
	5300 5400 4950 5400
$Comp
L Switch:SW_Push SW_Single_Step1
U 1 1 62943D46
P 3800 5400
F 0 "SW_Single_Step1" H 3800 5593 50  0000 C CNN
F 1 "SW_Push" H 3800 5594 50  0001 C CNN
F 2 "" H 3800 5600 50  0001 C CNN
F 3 "~" H 3800 5600 50  0001 C CNN
	1    3800 5400
	-1   0    0    -1  
$EndComp
$Comp
L Switch:SW_SPST SW_Manual_Control1
U 1 1 62942EAC
P 4750 5400
F 0 "SW_Manual_Control1" H 4750 5543 50  0000 C CNN
F 1 "SW_SPST" H 4750 5544 50  0001 C CNN
F 2 "" H 4750 5400 50  0001 C CNN
F 3 "~" H 4750 5400 50  0001 C CNN
	1    4750 5400
	-1   0    0    -1  
$EndComp
$Comp
L Device:R_Variable_US R_Clock_Speed1
U 1 1 628FB62E
P 5300 4950
F 0 "R_Clock_Speed1" H 4650 5000 50  0000 L CNN
F 1 "10K" H 5050 4900 50  0000 L CNN
F 2 "" V 5230 4950 50  0001 C CNN
F 3 "~" H 5300 4950 50  0001 C CNN
	1    5300 4950
	1    0    0    -1  
$EndComp
Wire Wire Line
	8450 4400 8350 4400
Connection ~ 8450 4400
Wire Wire Line
	8450 3550 8450 4400
Connection ~ 9400 4300
Wire Wire Line
	9400 4300 9650 4300
$Comp
L power:+5V #PWR0103
U 1 1 62C9AF0A
P 8650 4200
F 0 "#PWR0103" H 8650 4050 50  0001 C CNN
F 1 "+5V" H 8665 4373 50  0000 C CNN
F 2 "" H 8650 4200 50  0001 C CNN
F 3 "" H 8650 4200 50  0001 C CNN
	1    8650 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	8650 4400 8450 4400
Text GLabel 8450 3550 1    50   Output ~ 0
~CLK
Wire Wire Line
	9400 4300 9250 4300
Wire Wire Line
	9400 3550 9400 4300
Wire Wire Line
	3250 3500 3350 3500
Connection ~ 3250 3500
Wire Wire Line
	3250 3100 3550 3100
Wire Wire Line
	3250 3500 3250 3100
$Comp
L power:+5V #PWR0104
U 1 1 62C5091B
P 7500 4000
F 0 "#PWR0104" H 7500 3850 50  0001 C CNN
F 1 "+5V" H 7515 4173 50  0000 C CNN
F 2 "" H 7500 4000 50  0001 C CNN
F 3 "" H 7500 4000 50  0001 C CNN
	1    7500 4000
	1    0    0    -1  
$EndComp
Connection ~ 7500 4300
Wire Wire Line
	7500 4300 7500 4600
Wire Wire Line
	7750 4300 7500 4300
$Comp
L power:GND #PWR0105
U 1 1 62C4E41F
P 7500 4900
F 0 "#PWR0105" H 7500 4650 50  0001 C CNN
F 1 "GND" H 7505 4727 50  0000 C CNN
F 2 "" H 7500 4900 50  0001 C CNN
F 3 "" H 7500 4900 50  0001 C CNN
	1    7500 4900
	1    0    0    -1  
$EndComp
$Comp
L Device:CP1 C5
U 1 1 62C4D2FF
P 7500 4750
F 0 "C5" H 7615 4796 50  0000 L CNN
F 1 "10u" H 7615 4705 50  0000 L CNN
F 2 "" H 7500 4750 50  0001 C CNN
F 3 "~" H 7500 4750 50  0001 C CNN
	1    7500 4750
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R8
U 1 1 62C4AEDC
P 7500 4150
F 0 "R8" H 7568 4196 50  0000 L CNN
F 1 "1K" H 7568 4105 50  0000 L CNN
F 2 "" V 7540 4140 50  0001 C CNN
F 3 "~" H 7500 4150 50  0001 C CNN
	1    7500 4150
	1    0    0    -1  
$EndComp
$Comp
L 4xxx:4011 U2
U 4 1 62C30AC5
P 8050 4400
F 0 "U2" H 8050 4725 50  0000 C CNN
F 1 "4011" H 8050 4634 50  0000 C CNN
F 2 "" H 8050 4400 50  0001 C CNN
F 3 "http://www.intersil.com/content/dam/Intersil/documents/cd40/cd4011bms-12bms-23bms.pdf" H 8050 4400 50  0001 C CNN
	4    8050 4400
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R3
U 1 1 62912474
P 9950 4450
F 0 "R3" H 9882 4404 50  0000 R CNN
F 1 "220R" H 9882 4495 50  0000 R CNN
F 2 "" V 9990 4440 50  0001 C CNN
F 3 "~" H 9950 4450 50  0001 C CNN
	1    9950 4450
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D1
U 1 1 62922F24
P 9800 4300
F 0 "D1" H 9793 4045 50  0000 C CNN
F 1 "GREEN LED" H 9793 4136 50  0000 C CNN
F 2 "" H 9800 4300 50  0001 C CNN
F 3 "~" H 9800 4300 50  0001 C CNN
	1    9800 4300
	-1   0    0    1   
$EndComp
Text GLabel 9400 3550 1    50   Output ~ 0
CLK
Text GLabel 4550 2400 1    50   Output ~ 0
~RST
Wire Wire Line
	4550 3000 4550 2400
Wire Wire Line
	4400 3000 4550 3000
$Comp
L power:+5V #PWR0106
U 1 1 62C0D0D6
P 3800 2900
F 0 "#PWR0106" H 3800 2750 50  0001 C CNN
F 1 "+5V" H 3815 3073 50  0000 C CNN
F 2 "" H 3800 2900 50  0001 C CNN
F 3 "" H 3800 2900 50  0001 C CNN
	1    3800 2900
	1    0    0    -1  
$EndComp
Text GLabel 3550 2400 1    50   Output ~ 0
RST
Wire Wire Line
	3550 3100 3800 3100
Connection ~ 3550 3100
Wire Wire Line
	3550 2400 3550 3100
$Comp
L power:+5V #PWR0107
U 1 1 62BE1E73
P 1200 6400
F 0 "#PWR0107" H 1200 6250 50  0001 C CNN
F 1 "+5V" H 1215 6573 50  0000 C CNN
F 2 "" H 1200 6400 50  0001 C CNN
F 3 "" H 1200 6400 50  0001 C CNN
	1    1200 6400
	1    0    0    -1  
$EndComp
$Comp
L 4xxx:4011 U2
U 5 1 62BDF722
P 1200 6900
F 0 "U2" H 1430 6946 50  0000 L CNN
F 1 "4011" H 1430 6855 50  0000 L CNN
F 2 "" H 1200 6900 50  0001 C CNN
F 3 "http://www.intersil.com/content/dam/Intersil/documents/cd40/cd4011bms-12bms-23bms.pdf" H 1200 6900 50  0001 C CNN
	5    1200 6900
	1    0    0    -1  
$EndComp
$Comp
L 4xxx:4011 U2
U 3 1 62BDCE81
P 8950 4300
F 0 "U2" H 8950 4625 50  0000 C CNN
F 1 "4011" H 8950 4534 50  0000 C CNN
F 2 "" H 8950 4300 50  0001 C CNN
F 3 "http://www.intersil.com/content/dam/Intersil/documents/cd40/cd4011bms-12bms-23bms.pdf" H 8950 4300 50  0001 C CNN
	3    8950 4300
	1    0    0    -1  
$EndComp
$Comp
L 4xxx:4011 U2
U 1 1 62BDA9AA
P 4100 3000
F 0 "U2" H 4100 3325 50  0000 C CNN
F 1 "4011" H 4100 3234 50  0000 C CNN
F 2 "" H 4100 3000 50  0001 C CNN
F 3 "http://www.intersil.com/content/dam/Intersil/documents/cd40/cd4011bms-12bms-23bms.pdf" H 4100 3000 50  0001 C CNN
	1    4100 3000
	1    0    0    -1  
$EndComp
Connection ~ 1550 4400
Wire Wire Line
	1550 4400 1850 4400
NoConn ~ 3200 3700
Connection ~ 2000 3250
Wire Wire Line
	2700 3250 2700 3300
Wire Wire Line
	2000 3250 2700 3250
Wire Wire Line
	2000 3700 2000 3250
Connection ~ 2000 3700
Wire Wire Line
	2000 3900 2000 3700
Wire Wire Line
	3250 3900 3250 4400
Wire Wire Line
	1850 4400 3250 4400
Wire Wire Line
	2000 3900 2200 3900
$Comp
L Timer:LM555 U3
U 1 1 62BCC61C
P 2700 3700
F 0 "U3" H 2700 4281 50  0001 C CNN
F 1 "LM555" H 2450 4100 50  0000 C CNN
F 2 "" H 2700 3700 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm555.pdf" H 2700 3700 50  0001 C CNN
	1    2700 3700
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C4
U 1 1 62BCC612
P 2100 3700
F 0 "C4" H 2192 3746 50  0000 L CNN
F 1 "1u" H 2192 3655 50  0000 L CNN
F 2 "" H 2100 3700 50  0001 C CNN
F 3 "~" H 2100 3700 50  0001 C CNN
	1    2100 3700
	0    1    1    0   
$EndComp
Wire Wire Line
	1850 3500 2200 3500
Wire Wire Line
	1550 4400 1350 4400
Wire Wire Line
	3200 3500 3250 3500
$Comp
L power:+5V #PWR0108
U 1 1 62BCC5EC
P 1550 4100
F 0 "#PWR0108" H 1550 3950 50  0001 C CNN
F 1 "+5V" H 1565 4273 50  0000 C CNN
F 2 "" H 1550 4100 50  0001 C CNN
F 3 "" H 1550 4100 50  0001 C CNN
	1    1550 4100
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR0109
U 1 1 62BCC5E2
P 950 4400
F 0 "#PWR0109" H 950 4150 50  0001 C CNN
F 1 "GND" H 955 4227 50  0000 C CNN
F 2 "" H 950 4400 50  0001 C CNN
F 3 "" H 950 4400 50  0001 C CNN
	1    950  4400
	-1   0    0    -1  
$EndComp
$Comp
L Device:R_US R5
U 1 1 62BCC5D8
P 1550 4250
F 0 "R5" H 1618 4296 50  0000 L CNN
F 1 "1K" H 1618 4205 50  0000 L CNN
F 2 "" V 1590 4240 50  0001 C CNN
F 3 "~" H 1550 4250 50  0001 C CNN
	1    1550 4250
	-1   0    0    -1  
$EndComp
$Comp
L Switch:SW_Push SW_Reset1
U 1 1 62BCC5CE
P 1150 4400
F 0 "SW_Reset1" H 1150 4593 50  0000 C CNN
F 1 "SW_Push" H 1150 4594 50  0001 C CNN
F 2 "" H 1150 4600 50  0001 C CNN
F 3 "~" H 1150 4600 50  0001 C CNN
	1    1150 4400
	-1   0    0    -1  
$EndComp
Wire Wire Line
	3250 3900 3200 3900
Connection ~ 1850 4400
Wire Wire Line
	1850 4400 1850 3500
$Comp
L Device:LED D2
U 1 1 62BCC5B7
P 3500 3500
F 0 "D2" H 3493 3245 50  0000 C CNN
F 1 "YELLOW LED" H 3493 3336 50  0000 C CNN
F 2 "" H 3500 3500 50  0001 C CNN
F 3 "~" H 3500 3500 50  0001 C CNN
	1    3500 3500
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0110
U 1 1 62BCC5AD
P 3650 3800
F 0 "#PWR0110" H 3650 3550 50  0001 C CNN
F 1 "GND" H 3655 3627 50  0000 C CNN
F 2 "" H 3650 3800 50  0001 C CNN
F 3 "" H 3650 3800 50  0001 C CNN
	1    3650 3800
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R6
U 1 1 62BCC5A3
P 3650 3650
F 0 "R6" H 3582 3604 50  0000 R CNN
F 1 "220R" H 3582 3695 50  0000 R CNN
F 2 "" V 3690 3640 50  0001 C CNN
F 3 "~" H 3650 3650 50  0001 C CNN
	1    3650 3650
	-1   0    0    1   
$EndComp
$Comp
L power:+5V #PWR0112
U 1 1 62BCC570
P 2000 3250
F 0 "#PWR0112" H 2000 3100 50  0001 C CNN
F 1 "+5V" H 2015 3423 50  0000 C CNN
F 2 "" H 2000 3250 50  0001 C CNN
F 3 "" H 2000 3250 50  0001 C CNN
	1    2000 3250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0113
U 1 1 62BCC566
P 2700 4100
F 0 "#PWR0113" H 2700 3850 50  0001 C CNN
F 1 "GND" H 2705 3927 50  0000 C CNN
F 2 "" H 2700 4100 50  0001 C CNN
F 3 "" H 2700 4100 50  0001 C CNN
	1    2700 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	7300 4000 7300 4700
Wire Wire Line
	5300 4000 7300 4000
Connection ~ 6050 4250
Wire Wire Line
	6050 4250 6750 4250
Wire Wire Line
	7300 4900 7300 5400
Wire Wire Line
	5300 5100 5300 5400
Wire Wire Line
	5550 5400 7300 5400
Wire Wire Line
	5550 5400 5300 5400
Wire Wire Line
	5300 4800 5300 4600
Wire Wire Line
	5300 4000 5300 4300
$Comp
L Device:R_US R1
U 1 1 628FC499
P 5300 4450
F 0 "R1" H 5100 4500 50  0000 L CNN
F 1 "3R" H 5100 4400 50  0000 L CNN
F 2 "" V 5340 4440 50  0001 C CNN
F 3 "~" H 5300 4450 50  0001 C CNN
	1    5300 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	4300 5400 4000 5400
Connection ~ 4300 5400
Wire Wire Line
	4550 5400 4300 5400
$Comp
L power:+5V #PWR08
U 1 1 629463F7
P 4300 5100
F 0 "#PWR08" H 4300 4950 50  0001 C CNN
F 1 "+5V" H 4315 5273 50  0000 C CNN
F 2 "" H 4300 5100 50  0001 C CNN
F 3 "" H 4300 5100 50  0001 C CNN
	1    4300 5100
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR09
U 1 1 62945069
P 3600 5400
F 0 "#PWR09" H 3600 5150 50  0001 C CNN
F 1 "GND" H 3605 5227 50  0000 C CNN
F 2 "" H 3600 5400 50  0001 C CNN
F 3 "" H 3600 5400 50  0001 C CNN
	1    3600 5400
	-1   0    0    -1  
$EndComp
$Comp
L Device:R_US R4
U 1 1 629447A7
P 4300 5250
F 0 "R4" H 4368 5296 50  0000 L CNN
F 1 "1K" H 4368 5205 50  0000 L CNN
F 2 "" V 4340 5240 50  0001 C CNN
F 3 "~" H 4300 5250 50  0001 C CNN
	1    4300 5250
	-1   0    0    -1  
$EndComp
Connection ~ 5550 5400
Wire Wire Line
	5550 5400 5550 4500
$Comp
L power:GND #PWR07
U 1 1 62914FED
P 9950 4600
F 0 "#PWR07" H 9950 4350 50  0001 C CNN
F 1 "GND" H 9955 4427 50  0000 C CNN
F 2 "" H 9950 4600 50  0001 C CNN
F 3 "" H 9950 4600 50  0001 C CNN
	1    9950 4600
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR06
U 1 1 62902735
P 5300 3700
F 0 "#PWR06" H 5300 3550 50  0001 C CNN
F 1 "+5V" H 5315 3873 50  0000 C CNN
F 2 "" H 5300 3700 50  0001 C CNN
F 3 "" H 5300 3700 50  0001 C CNN
	1    5300 3700
	1    0    0    -1  
$EndComp
$Comp
L Device:R_US R2
U 1 1 629020C1
P 5300 3850
F 0 "R2" H 5368 3896 50  0000 L CNN
F 1 "220R" H 5368 3805 50  0000 L CNN
F 2 "" V 5340 3840 50  0001 C CNN
F 3 "~" H 5300 3850 50  0001 C CNN
	1    5300 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	5550 5550 5550 5400
$Comp
L Device:CP1 C1
U 1 1 628F2310
P 5550 5700
F 0 "C1" H 5665 5746 50  0000 L CNN
F 1 "10u" H 5665 5655 50  0000 L CNN
F 2 "" H 5550 5700 50  0001 C CNN
F 3 "~" H 5550 5700 50  0001 C CNN
	1    5550 5700
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR04
U 1 1 628F1BE6
P 6050 4250
F 0 "#PWR04" H 6050 4100 50  0001 C CNN
F 1 "+5V" H 6065 4423 50  0000 C CNN
F 2 "" H 6050 4250 50  0001 C CNN
F 3 "" H 6050 4250 50  0001 C CNN
	1    6050 4250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR01
U 1 1 628F2EE8
P 5550 5850
F 0 "#PWR01" H 5550 5600 50  0001 C CNN
F 1 "GND" H 5555 5677 50  0000 C CNN
F 2 "" H 5550 5850 50  0001 C CNN
F 3 "" H 5550 5850 50  0001 C CNN
	1    5550 5850
	1    0    0    -1  
$EndComp
Wire Wire Line
	1850 4550 1850 4400
$Comp
L Device:CP1 C3
U 1 1 62BCC57A
P 1850 4700
F 0 "C3" H 1965 4746 50  0000 L CNN
F 1 "10u" H 1965 4655 50  0000 L CNN
F 2 "" H 1850 4700 50  0001 C CNN
F 3 "~" H 1850 4700 50  0001 C CNN
	1    1850 4700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0111
U 1 1 62BCC584
P 1850 4850
F 0 "#PWR0111" H 1850 4600 50  0001 C CNN
F 1 "GND" H 1855 4677 50  0000 C CNN
F 2 "" H 1850 4850 50  0001 C CNN
F 3 "" H 1850 4850 50  0001 C CNN
	1    1850 4850
	1    0    0    -1  
$EndComp
$EndSCHEMATC
