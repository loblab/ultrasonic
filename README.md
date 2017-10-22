# Ultrasonic Height Meter

Use Ultrasonic sensor (HC-SR04) to measure/monitor height

- Platform: Raspberry Pi (Debian 9.x), HC-SR04
- Ver: 0.1
- Updated: 10/22/2017
- Created: 10/15/2017
- Author: loblab

![Ultrasonic with Raspberry Pi](https://raw.githubusercontent.com/loblab/ultrasonic/master/ultrasonic.jpg)

## Ultrasonic sensor (HC-SR04)

HC-SR04 has TRIG (CH0) & ECHO (CH1) pin

![Waveform overview](https://raw.githubusercontent.com/loblab/ultrasonic/master/waveform1.png)

distance = pluse width * sonic speed / 2 

![Waveform details](https://raw.githubusercontent.com/loblab/ultrasonic/master/waveform2.png)

(waveform above) = 2.8924 / 1000 * 343 / 2 = 0.496 (m)

## History

- 0.1 (10/22/2017) : Basic distance measurement, multi-threading

