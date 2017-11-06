"""
Parker Williamson & Ryan Jones
ME 507 - Cue Following Vehicle Project

10/31/16

This project controls a RC car using commands on a USB key board or following
cues that it finds around it (such as staying in its lane and follow stop sign
instructions).


python3 /home/pi/Documents/ME_507_Project/main.py

"""

#from time import sleep

#import shared variables
import config

#import other tasks
import task_runCar

#initiate a runCar instance
car = task_runCar.car()

#loop until user hits 'q' and causes 
while (config.esc == 0):
    #loop task_runCar to control other tasks
    car.carControlLoop()
    

