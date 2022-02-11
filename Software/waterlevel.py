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

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) #水位传感器接口

class water:
    def getwaterlevel(pin):

            waterlevelstate = GPIO.input(pin)
            if waterlevelstate == 1:
                return waterlevelstate
            else:
                return waterlevelstate