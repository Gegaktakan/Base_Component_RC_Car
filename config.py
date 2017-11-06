"""

All the shared variables are declared here and this file needs to be imported
into any file which needs these variables just needs to import sharedVar

"""
# Import the PCA9685 module.
import Adafruit_PCA9685


speed = 0   # speed of the motor (0-4096 representing the percentage of
                                    #frequecy that the pulse width is)
ang = ((310.0+490)/2) # angle of the serveo (310-490 pulse width size)
runMode = 0  # (0) brake, (1) manual, (2) image recognition
esc = 0   # set to 1 in order to esc all shared multitasking loops
Color = -1 # stop light color indicator

pwm = Adafruit_PCA9685.PCA9685() # Initiate pwm chip communication
pwm.set_pwm_freq(50) # Set pwm frequency to 50 Hz so that it can control both
                            #the servo and the motor
