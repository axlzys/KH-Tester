import time
import sys

_temperature      = 25.0
_acidVoltage      = 2032.44
_neutralVoltage   = 1500.0
class DFRobot_PH():
	def begin(self):
		global _acidVoltage
		global _neutralVoltage
		try:
			with open('/home/pi/APP/examples/examples/templates/phdata.txt','r') as f:
				neutralVoltageLine = f.readline()
				neutralVoltageLine = neutralVoltageLine.strip('neutralVoltage=')
				_neutralVoltage    = float(neutralVoltageLine)
				acidVoltageLine    = f.readline()
				acidVoltageLine    = acidVoltageLine.strip('acidVoltage=')
				_acidVoltage       = float(acidVoltageLine)
		except :
			print ("/home/pi/APP/examples/examples/templates/phdata.txt ERROR ! Please run DFRobot_PH_Reset")
			sys.exit(1)
			
	def readPH(self,voltage,temperature):
		global _acidVoltage
		global _neutralVoltage
		slope     = (7.0-4.0)/((_neutralVoltage-1500.0)/3.0 - (_acidVoltage-1500.0)/3.0)
		intercept = 7.0 - slope*(_neutralVoltage-1500.0)/3.0
		_phValue  = slope*(voltage-1500.0)/3.0+intercept
		round(_phValue,2)
		return _phValue

	def calibration(self,voltage):
		if (voltage>1322 and voltage<1778):
			print (">>>Buffer Solution:7.0")
			f=open('/home/pi/APP/examples/examples/templates/phdata.txt','r+')
			flist=f.readlines()
			flist[0]='neutralVoltage='+ str(voltage) + '\n'
			f=open('/home/pi/APP/examples/examples/templates/phdata.txt','w+')
			f.writelines(flist)
			f.close()
			return ">>>PH:7.0校准成功！"

		elif (voltage>1854 and voltage<2210):
			print (">>>Buffer Solution:4.0")
			f=open('/home/pi/APP/examples/examples/templates/phdata.txt','r+')
			flist=f.readlines()
			flist[1]='acidVoltage='+ str(voltage) + '\n'
			f=open('/home/pi/APP/examples/examples/templates/phdata.txt','w+')
			f.writelines(flist)
			f.close()
			return ">>>PH:4.0校准成功！"
		else:
			return ">>>PH标准液错误，请重试！"


	def reset(self):
		_acidVoltage    = 2032.44
		_neutralVoltage = 1500.0
		try:
			f=open('/home/pi/APP/examples/examples/templates/phdata.txt','r+')
			flist=f.readlines()
			flist[0]='neutralVoltage='+ str(_neutralVoltage) + '\n'
			flist[1]='acidVoltage='+ str(_acidVoltage) + '\n'
			f=open('phdata.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>Reset to default parameters<<<")
		except:
			f=open('//home/pi/APP/examples/examples/templates/phdata.txt','w')
			#flist=f.readlines()
			flist   ='neutralVoltage='+ str(_neutralVoltage) + '\n'
			flist  +='acidVoltage='+ str(_acidVoltage) + '\n'
			#f=open('data.txt','w+')
			f.writelines(flist)
			f.close()
			print (">>>Reset to default parameters<<<")