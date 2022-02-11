#                 This software is part of the KH Tester
#                               Version 3.0
#                   Copyright (C) 2022 jiawei wu
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License version 3 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# version 3 along with this program in the file "LICENSE".  If not, see
# <http://www.gnu.org/licenses/agpl-3.0.txt>.

import time
import board
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from waterlevel import water
from DFRobot_ADS1115 import ADS1115
from DFRobot_PH import DFRobot_PH

device_file ='/sys/bus/w1/devices/28-00000da16ae3/w1_slave'


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

GPIO.output(22,False)
GPIO.output(23, False)
ads1115 = ADS1115()
ph = DFRobot_PH()
kit = MotorKit(i2c=board.I2C())
kit.motor1.throttle = 0
kit.motor2.throttle = 0
kit.motor3.throttle = 0
kit.motor4.throttle = 0

class tester:
    def fillbot(self):
        begin = time.time()
        while water.getwaterlevel(17) != 1:
            now = time.time()

            if now - begin <= 50:
                kit.motor1.throttle = 1
            else:
                kit.motor1.throttle = 0
                return False
        else:
            kit.motor1.throttle = 0

    def fillbot1(self):
            while water.getwaterlevel(17) != 1:
                kit.motor1.throttle = 1
            else:
                kit.motor1.throttle = 0

    def drainbot(self):
        kit.motor2.throttle = 1.0
        time.sleep(90)
        kit.motor2.throttle = 0

    def cleanbot(self):
        tester().fillbot()
        GPIO.output(22, True)
        GPIO.output(23, False)
        time.sleep(20)
        GPIO.output(22, False)
        GPIO.output(23, False)
        tester().drainbot()
        return "反应仓清洗完毕！"

    def readPH(self,pin):
        temperature = 25
        ads1115.setAddr_ADS1115(0x49)
        ads1115.setGain(0x00)
        ph.begin()
        adc0 = ads1115.readVoltage(pin)
        PH = ph.readPH(adc0['r'], temperature)
        return round(PH,2)

    def CalibrationPH(self,pin):
        temperature = 25
        ads1115.setAddr_ADS1115(0x49)
        # Sets the gain and input voltage range.
        ads1115.setGain(0x00)
        # Get the Digital Value of Analog of selected channel
        adc0 = ads1115.readVoltage(pin)
        #print("A0:%dmV "%(adc0['r']))
        PH = ph.calibration(adc0['r'])
        time.sleep(1.0)
        return PH

    def aaa(self):

         a = 0
         while a<10:
             for i in range(10):
                kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
             if GPIO.event_detected(18):
                 a=a+1
         else:
             kit.stepper2.release()
         return a

    def getRespose(self):
        kit.motor3.throttle = 0




    GPIO.add_event_detect(18, GPIO.FALLING)
    GPIO.add_event_callback(18, getRespose)

    def testpwm(self):
        '''GPIO.setmode(GPIO.BCM)
        GPIO.setup(24, GPIO.OUT)
        p = GPIO.PWM(24, 100)
        p.start(100)
        time.sleep(20.0)
        p.stop()
        GPIO.cleanup()
        ii = 0
        Drops.query.delete()
        while ii < 2:
            kit.motor1.throttle = 0.45
            if GPIO.event_detected(18):
                ii = ii + 1
                Drop = Drops(Date=datetime.now().strftime('%Y-%m-%d'), Time=datetime.now().strftime('%H:%M:%S'),
                                 Drops=ii)
                db.session.add(Drop)
                db.session.commit()
                time.sleep(1.5)
        else:
            kit.motor1.throttle = 00
        return ii'''


        tester().fillbot()
        GPIO.output(22, True)
        GPIO.output(23, False)
        time.sleep(30)
        ii = 0
        aa = tester().readPH()
        while aa >= 4.5:
        #while ii<100:

            kit.motor3.throttle = 0.6
            if GPIO.event_detected(18):
                ii = ii + 1
            aa = tester().readPH()
            time.sleep(1)
        else:
            kit.motor3.throttle = 0
            GPIO.output(22, False)
            GPIO.output(23, False)
        return ii



    def KHtester(self):
        tester().drainbot()
        if tester().fillbot() != False:
            GPIO.output(22, True)
            GPIO.output(23, False)
            time.sleep(30)
            GPIO.output(22, False)
            GPIO.output(23, False)
            tester().drainbot()
            if tester().fillbot() != False:
                GPIO.output(22, True)
                GPIO.output(23, False)
                time.sleep(30)
                #kit.motor4.throttle = 0
                ii = 0
            #aa = tester().readPH(1)
                while tester().readPH(1) >= 4.5:
                    kit.motor3.throttle = 0.6
                    if GPIO.event_detected(18):
                        ii = ii + 1
                    #kit.motor4.throttle = 0.2
                    time.sleep(1.5)
                   # kit.motor4.throttle = 0
                   # time.sleep(1)
                else:
                    kit.motor3.throttle = 0
                    GPIO.output(22, False)
                    GPIO.output(23, False)
                return ii
            else:
                return False
        else:
            return False

    def CalibrationACIVcore(self):
        iii = 0
        while iii < 100:
            kit.motor3.throttle = 0.6
            if GPIO.event_detected(18):
                iii = iii + 1
            time.sleep(1.5)
        else:
            kit.motor3.throttle = 0
        return iii

    def pharmacypump(self,status):
        if status == 1:
            kit.motor3.throttle = 1
        elif status == 0:
            kit.motor3.throttle = 0

    def Inpumpon(self):
        kit.motor1.throttle = 1

    def Inpumpoff(self):
        kit.motor1.throttle = 0

    def Outpumpon(self):
        kit.motor2.throttle = 1

    def Outpumpoff(self):
        kit.motor2.throttle = 0

    def KHpumpon(self):
        kit.motor4.throttle = 1

    def KHpumpoff(self):
        kit.motor4.throttle = 0

    def pharmacypumpon(self):
        kit.motor3.throttle = 0.6

    def pharmacypumpoff(self):
        kit.motor3.throttle = 0

    def stir(self):
        GPIO.output(22, True)
        GPIO.output(23, False)
        time.sleep(15)
        GPIO.output(22, False)
        GPIO.output(23, False)
