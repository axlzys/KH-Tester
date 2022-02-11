import sys
sys.path.append('../')
import time

from DFRobot_ADS1115 import ADS1115
from DFRobot_PH      import DFRobot_PH

ads1115 = ADS1115()
ph      = DFRobot_PH()

ph.begin()
while True :
	temperature = 20
	#Set the IIC address
	ads1115.setAddr_ADS1115(0x49)
	#Sets the gain and input voltage range.
	ads1115.setGain(0x00)
	#Get the Digital Value of Analog of selected channel
	adc0 = ads1115.readVoltage(1)
	print ("A0:%dmV "%(adc0['r']))
	#Calibrate the calibration data
	ph.calibration(adc0['r'])
	time.sleep(1.0)
