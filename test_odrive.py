#!/usr/bin/python
# author achuwils

import piggy_odrive
import math
import time

from odrive.enums import *


motors= piggy_odrive.piggydrive()

#wait until motors complete homing 
while(motors.isReady==False):
    time.sleep(0.5)

#print the current joint position
#motors.axis0.requested_state = AXIS_STATE_IDLE
#motors.axis1.requested_state = AXIS_STATE_IDLE
#motors.axis2.requested_state = AXIS_STATE_IDLE

print "current position is ", motors.getJointPos()



'''

#set all joints to 45 degree
#setJointPosWait is a blocking call. It will return true when it reaches the position
#the arguments are 3 joints values in radians, passed as a list
motors.setJointPosWait([math.radians(-40),math.radians(-40),math.radians(-40)])
time.sleep(1)
print "current position is ", motors.getJointPos()

motors.setJointPosWait([math.radians(-20),math.radians(-20),math.radians(-20)])
time.sleep(1)
print "current position is ", motors.getJointPos()


motors.setJointPosWait([math.radians(0),math.radians(0),math.radians(0)])
time.sleep(1)
print "current position is ", motors.getJointPos()

motors.setJointPosWait([math.radians(45),math.radians(45),math.radians(45)])
time.sleep(1)
print "current position is ", motors.getJointPos()


motors.setJointPosWait([math.radians(90),math.radians(90),math.radians(90)])
time.sleep(1)
print "current position is ", motors.getJointPos()

motors.setJointPosWait([math.radians(115),math.radians(115),math.radians(115)])
time.sleep(1)
print "current position is ", motors.getJointPos()


motors.setJointPosWait([math.radians(90),math.radians(90),math.radians(90)])
time.sleep(1)
print "current position is ", motors.getJointPos()

motors.setJointPosWait([math.radians(45),math.radians(45),math.radians(45)])
time.sleep(1)
print "current position is ", motors.getJointPos()


'''