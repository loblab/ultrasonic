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

import RPi.GPIO as GPIO 
import time 
import threading

class Sensor(threading.Thread):

    HALF_SONIC_SPEED = 171.5  # 20 °C in air

    def __init__(self, name, pin_echo, pin_trig):
        threading.Thread.__init__(self)
        GPIO.setup(pin_trig, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(pin_echo, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.name = name
        self.pin_echo = pin_echo
        self.pin_trig = pin_trig
        self.time = 0
        self.dist = 0

    def trigger(self, width=10e-6):
        t1 = time.time()
        GPIO.output(self.pin_trig, GPIO.HIGH)
        t2 = time.time()
        wait = t2 - t1 - width
        if wait > 0:
            time.sleep(wait)
        GPIO.output(self.pin_trig, GPIO.LOW)

    def measure(self, timeout_leading=5, timeout_pluse=30):
        ch = GPIO.wait_for_edge(self.pin_echo, GPIO.RISING, timeout=timeout_leading)
        t1 = time.time()
        if ch is None:
            tstr = time.strftime('%H:%M:%S', time.localtime(self.time))
            #print "[%s] %s - timeout 1" % (self.name, tstr)
            #return None
        ch = GPIO.wait_for_edge(self.pin_echo, GPIO.FALLING, timeout=timeout_pluse)
        t2 = time.time()
        if ch is None:
            #tstr = time.strftime('%H:%M:%S', time.localtime(self.time))
            #print "[%s] %s - timeout 2" % (self.name, tstr)
            return None
        self.time = (t2 + t1) / 2
        self.dist = (t2 - t1) * Sensor.HALF_SONIC_SPEED
        return self.dist

    def show(self):
        tstr = time.strftime('%H:%M:%S', time.localtime(self.time))
        print "[%s] %s - %.3f" % (self.name, tstr, self.dist)

    def run(self):
        #self.active_flag.set()
        self.count = 0
        self.sum = 0.0
        while self.enabled:
            dist = self.measure(500)
            if dist is None:
                continue
            self.sum += dist
            self.count += 1
            self.show()
        if self.count > 0:
            tstr = time.strftime('%H:%M:%S', time.localtime(self.time))
            print "[%s] %s - %.3f (Average of %d times)" % (self.name, tstr, self.sum / self.count, self.count)

    def enable(self, en=True):
        self.enabled = en
        if en:
            #self.active_flag = threading.Event()
            #self.active_flag.clear()
            self.start()
            #self.active_flag.wait()
            time.sleep(0.1)  # wait the thread starting
        else:
            self.join()

