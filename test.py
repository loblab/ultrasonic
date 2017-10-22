#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2017 loblab
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from config import *
from sensor import *
from program import *

VERSION = "Ver 0.1, 10/15/2017, loblab"

class Program(ProgramBase):

    def init_arguments(self):
        self.argps.add_argument('-l', dest='log', action='store_true',
            help="log messages to text log file (LOG_FILE in config.py)")
        self.argps.add_argument('-d', dest='debug', type=int, default=0, choices=range(3),
            help="debug info level, greater for more. default 0")
        self.argps.add_argument('-r', dest='repeat', type=int, default=10,
            help="repeat count. default 10")
        self.argps.add_argument('-i', dest='interval', type=int, default=20,
            help="interval during 2 measurement. default 10")

    def init_device(self):
        self.sensor = Sensor('Height', PIN_DIST_ECHO, PIN_DIST_TRIG)

    def process(self):
        self.sensor.enable(True)
        for i in range(self.args.repeat):
            if self.quit_flag:
                break
            self.sensor.trigger()
            #print i + 1
            time.sleep(self.args.interval * 1e-3)
        self.sensor.enable(False)
        return 0


if __name__ == "__main__":
    prog = Program("USHM", VERSION, "Ultrasonic height meter", LOG_FILE)
    sys.exit(prog.main())

