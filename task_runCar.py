"""

task_runCar keeps track of all the run mode the car is in

"""

#import shared variables
import config

#import other classes
import task_user
import MotorControl
import ServoControl
import CameraProcess

class car:
    def __init__(self):
        #initiate user interface
        global user
        user = task_user.userInput()
        #initiate motor
        global motor
        motor = MotorControl.motorControl()
        #initiate servo
        global servo
        servo = ServoControl.servoControl()
        #initiate camera
        global camera
        camera = CameraProcess.cameraProcess()
        
    def carMode0(self): #stop/dont move
        motor.brake()
        
    def carMode1(self): #manual drive
        # Set Motor in different ways based on speed
        if(config.speed>0):
            motor.clockwiseSetSpeed(int(config.speed))
        elif(config.speed<0):
            motor.counterClockwiseSetSpeed(int(abs(config.speed)))
        elif(config.speed==0):
            motor.brake()
        # Set Servo 
        servo.ser_ang(int(config.ang))
        
    def carMode2(self): #cue following mode
        # Take an image and process it to set shared variables
        camera.takePhoto()
        # if not a yellow light speed is about 3/8th maximum
        if(config.Color!=2):
            config.speed =1500
            
        if (config.Color== 0):
            #if all 'powerOutage?' go backwards at 3/8ths maximum speed
            motor.counterClockwiseSetSpeed(int(abs(config.speed)))
        elif (config.Color== 1):
            #if red stop
            motor.brake()
        elif (config.Color== 2):
            #if yellow go forwards at maximum(-ish) speed
            config.speed =4000
            motor.clockwiseSetSpeed(int(config.speed))
        elif (config.Color== 3):
            #if green go forwards at normal speed
            motor.clockwiseSetSpeed(int(config.speed))

    def carControlLoop(self):
        user.check_input()
        
        #decifer mode
        if config.runMode == 0:
            self.carMode0()
        if config.runMode == 1:
            self.carMode1()
        if config.runMode == 2:
            self.carMode2()
        


