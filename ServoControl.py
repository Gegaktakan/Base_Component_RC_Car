#from __future__ import division
import time

#import for shared variables
import config

class servoControl:
    def __init__(self):
        global channelServo
        channelServo = 0
                
        # Configure min and max servo pulse lengths
        global servo_min
        global servo_max
        servo_min = 310  # Min pulse length out of 4096
        servo_max = 490  # Max pulse length out of 4096

    def ser_ang(self, angle):
        # Set servo angle and saturate at max and min
        if(angle>490):
            config.pwm.set_pwm(channelServo, 0, 490)
        elif(angle<310):
            config.pwm.set_pwm(channelServo, 0, 310)
        else:
            config.pwm.set_pwm(channelServo, 0, angle)

# Test servo setup
if __name__ == '__main__':
    b = servoControl()
    try:
        while True:
            b.ser_ang(490)
            time.sleep(1)
            print('1')
            b.ser_ang(445)
            time.sleep(1)
            print('2')
            b.ser_ang(400)
            time.sleep(1)
            print('3')
            b.ser_ang(355)
            time.sleep(1)
            print('4')
            b.ser_ang(310)
            time.sleep(1)
            print('5')
    except KeyboardInterrupt:
        print('done')
