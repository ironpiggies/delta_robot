#!/usr/bin/python
# author achuwils

import inverse_kinematics
#import piggy_odrive
import math
import time
from odrive.enums import *



class detlaBot:
    def __init__(self):
        self.RUN_REAL= True
        if self.RUN_REAL:
            import piggy_odrive   
            self.motors = piggy_odrive.piggydrive()
            while(self.motors.isReady==False):
                time.sleep(0.5)
            print "motors ready"
        self.kinsolver = inverse_kinematics.deltaSolver()
        self.kinsolver.plot()

    def moveXYZ(self, posval):
        '''
        move the robot in xyz coordinates
        input is a list having the [x,y,z] values in millimeters
        NOTE: z axis is negative downwards
        '''
        goalpos=inverse_kinematics.position(posval[0],posval[1],posval[2])
        try:
            cmdtheta = self.kinsolver.ik(goalpos)
            self.kinsolver.updatePlot(goalpos)
            if self.RUN_REAL:
                return self.motors.setJointPosWait(cmdtheta)
            else:
                return 2 
        except:
            print('Could not move')
            return 0
            
    def setHighSpeed(self):
        self.motors.setHighSpeed()

    def setLowSpeed(self):
        self.motors.setLowSpeed()
    



def main():
    robo= detlaBot()
    for i in range(5):
        #set low speed mode
        robo.setLowSpeed()
        #draw a rectange
        robo.moveXYZ([100,100,-700])
        robo.moveXYZ([100,-100,-700])
        robo.moveXYZ([-100,-100,-700])
        robo.moveXYZ([-100,100,-700])
    
        #set high speed mode
        #draw a rectange
        robo.setHighSpeed()
        robo.moveXYZ([100,100,-700])
        robo.moveXYZ([100,-100,-700])
        robo.moveXYZ([-100,-100,-700])
        robo.moveXYZ([-100,100,-700])





if __name__=="__main__":
    main()