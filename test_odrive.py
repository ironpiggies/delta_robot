#!/usr/bin/python
# author achuwils

import piggy_odrive
import math

motors= piggy_odrive.piggydrive()

#wait until motors complete homing 
while(motors.isReady==False):
    time.sleep(0.5)

#print the current joint position
print "current position is ", motors.getJointPos()

#set all joints to 45 degree
#setJointPosWait is a blocking call. It will return true when it reaches the position
#the arguments are 3 joints values in radians, passed as a list
motors.setJointPosWait([math.radians(90),math.radians(90),math.radians(90)])
