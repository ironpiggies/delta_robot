#!/usr/bin/python
'''
author achuwils
'''

import odrive
from odrive.enums import *
import time
import math


_HOMING_CURRENT_THRESHOLD = 1.35

#2084377A3548  o1
#2087377B3548  02

usb_serials = ['2087377B3548','2084377A3548']
odrvs = [None,None]
axes = [None, None, None]
axis0 = None
axis1 = None
axis2 = None

axis0_homepos= None
axis1_homepos= None
axis2_homepos= None

ready = False

CPR2RAD = (2*math.pi/400000.00)
CPR= 400000
MAX_LIMIT = math.pi




def get_joint_pos():
    '''
    Returns an array of the current joint positions in radians
    '''
    return[(axis0.encoder.pos_estimate - axis0_homepos)*CPR2RAD,(axis1.encoder.pos_estimate - axis1_homepos)*CPR2RAD,(axis2.encoder.pos_estimate - axis2_homepos)*CPR2RAD]

def set_joint_pos(posval):
    '''
    Set the joint position of three motors, argument is an array of angle values in radians
    '''
    #check whether all values are inside limit
    if((0<=posval[0]<=math.pi) and (0<=posval[0]<=math.pi) and (0<=posval[0]<=math.pi)): 
        print "setpos called", (posval[0]*CPR )/ (2* math.pi) + axis0_homepos,(posval[1]*CPR )/ (2* math.pi) + axis1_homepos,(posval[2]*CPR )/ (2* math.pi) + axis2_homepos
        axis0.controller.pos_setpoint = int((posval[0]*CPR )/ (2* math.pi) + axis0_homepos)
        axis1.controller.pos_setpoint = int((posval[1]*CPR )/ (2* math.pi) + axis1_homepos)
        axis2.controller.pos_setpoint = int((posval[2]*CPR )/ (2* math.pi) + axis2_homepos)
    else:
        print " commanded motor position out of safe limit"



def connect_all():
    '''
    Call this function at first to connect to odrives
    Note -  call it only after the motors complete the initial automatic calibration which 
    occurs after powering on
    '''
    global axis0, axis1, axis2, axes
    for ii in range(len(odrvs)):
        if usb_serials[ii] == None:
            continue
        print("searching odrive: " + usb_serials[ii]+ "...")
        odrvs[ii]= odrive.find_any(serial_number = usb_serials[ii])
        print("found odrive! " + str(ii))
    axis0 = odrvs[0].axis0
    axis1 = odrvs[0].axis1
    axis2 = odrvs[1].axis0
    axes[0] = axis0
    axes[1] = axis1
    axes[2] = axis2


connect_all()

time.sleep(1)

#set all three motors to velocity mode and rotate CW to look for home position
axis0.controller.config.control_mode =CTRL_MODE_VELOCITY_CONTROL
axis1.controller.config.control_mode =CTRL_MODE_VELOCITY_CONTROL
axis2.controller.config.control_mode =CTRL_MODE_VELOCITY_CONTROL

axis0.controller.vel_setpoint = 6000
axis1.controller.vel_setpoint = 6000
axis2.controller.vel_setpoint = 6000
time.sleep(1)

axis0_homed =False
axis1_homed =False
axis2_homed =False
'''
while(not(axis0_homed and axis1_homed and axis2_homed)):
    if( abs(axis0.motor.current_control.Iq_measured)>_HOMING_CURRENT_THRESHOLD and not(axis0_homed)):
        axis0.controller.vel_setpoint = 0
        axis0.controller.vel_setpoint = 0
        axis0_homed = True
        print "axis 0 homed"
    if( abs(axis1.motor.current_control.Iq_measured)>_HOMING_CURRENT_THRESHOLD and not(axis1_homed)):
        axis1.controller.vel_setpoint = 0
        axis1.controller.vel_setpoint = 0
        axis1_homed = True
        print "axis 1 homed"
    if( abs(axis2.motor.current_control.Iq_measured)>_HOMING_CURRENT_THRESHOLD and not(axis2_homed)):
        axis2.controller.vel_setpoint = 0
        axis2.controller.vel_setpoint = 0
        axis2_homed = True
        print "axis 2 homed" 
    time.sleep(0.01)    
    #print "Homing ..." , axis0.motor.current_control.Iq_measured,axis1.motor.current_control.Iq_measured,axis2.motor.current_control.Iq_measured
'''
print "Homing complete"
axis0_homepos= axis0.encoder.pos_estimate
axis1_homepos= axis0.encoder.pos_estimate
axis2_homepos= axis0.encoder.pos_estimate
print "Homing position set"


axis0.controller.pos_setpoint = axis0_homepos
axis1.controller.pos_setpoint = axis1_homepos
axis2.controller.pos_setpoint = axis2_homepos


print "switching to position control mode"
time.sleep(1)

axis0.controller.config.control_mode =CTRL_MODE_POSITION_CONTROL
axis1.controller.config.control_mode =CTRL_MODE_POSITION_CONTROL
axis2.controller.config.control_mode =CTRL_MODE_POSITION_CONTROL
time.sleep(1)

print "odrives are ready"
ready = True
