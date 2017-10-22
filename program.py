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

import sys
import time 
import signal
import argparse
import RPi.GPIO as GPIO 


class ProgramBase:

    def __init__(self, name, version, description, log_file):
        self.name = name
        self.log_file = log_file
        self.quit_flag = False
        signal.signal(signal.SIGINT, self.sig_handler)
        signal.signal(signal.SIGTERM, self.sig_handler)

        self.argps = argparse.ArgumentParser(version=version, description=description)
        self.init_arguments()
        self.args = self.argps.parse_args()

        GPIO.setmode(GPIO.BCM) 
        self.init_device()

    def cleanup(self):
        GPIO.cleanup()

    def log_msg(self, msg):
        tstr = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        with open(self.log_file, 'a') as fp:
            fp.write("%s [%s] - %s\r\n" % (tstr, self.name, msg))

    def sig_handler(self, signum, frame):
        msg = "Got system signal %d... quit now." % signum
        print msg
        if self.args.log:
            self.log_msg(msg)
        self.quit_flag = True

    def main(self):
        try:
            rc = self.process()
        finally:
            self.cleanup()
        return rc

