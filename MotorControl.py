#import GPIO for pin control
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#import config for shared variables
import config

class motorControl:
    def __init__(self):
        global motor_min
        motor_min = 1  # Min pulse length out of 4096
        global motor_max
        motor_max = 4095  # Max pulse length out of 4096
        global motor_channel
        motor_channel = 4  # Channel of the motor on the the pwm chip
        global InA
        InA = 17  # PI pin number of the chip that controls the InA of the h-bridge
        global InB
        InB = 27  # PI pin number of the chip that controls the InB of the h-bridge
        # Don't want it to warn if the pi's pins had been set in a previous run
        GPIO.setwarnings(False)
        # Set PI pins as outputs
        GPIO.setup(InA, GPIO.OUT)
        GPIO.setup(InB, GPIO.OUT)
        
    def clockwiseSetSpeed(self,speed):
        GPIO.output(InA, 1)
        GPIO.output(InB, 0)
        config.pwm.set_pwm(motor_channel, 0, speed)
        
    def counterClockwiseSetSpeed(self,speed):
        GPIO.output(InA, 0)
        GPIO.output(InB, 1)
        config.pwm.set_pwm(motor_channel, 0, speed)
        
    def brake(self):
        GPIO.output(InA, 1)
        GPIO.output(InB, 1)
        config.pwm.set_pwm(motor_channel, 0, 2000)
        
# Test motor setup
if __name__ == '__main__':
    a = motorControl()
    try:
        while True:
            a.clockwiseSetSpeed(2000)
            time.sleep(1)
            a.counterClockwiseSetSpeed(2000)
            time.sleep(1)
            a.brake()
            time.sleep(1)
            print('rep')
    except KeyboardInterrupt:
        print('worked?')
        GPIO.cleanup()
    
