#!/usr/bin/python
'''
author achuwils
for usage example, see test_odrive.py
'''

import odrive
from odrive.enums import *
import time
import math


_HOMING_CURRENT_THRESHOLD = 1.8
_POS_ERR_THRES = 0.008
_MAXPOS_LIMIT = math.pi

#2084377A3548  o1
#2087377B3548  02

usb_serials = ['2087377B3548','2084378A3548']
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

class piggydrive:
    def __init__(self):
        self.isReady = False
        print "Searching for odrive 1"
        self.odrv0=odrive.find_any(serial_number='2087377B3548')
        print "Searching for odrive 2"
        self.odrv1=odrive.find_any(serial_number='2084378A3548')
        print "odrives found"
        self.axis0 = self.odrv0.axis0
        self.axis1 = self.odrv0.axis1
        self.axis2 = self.odrv1.axis0
        #begin the homing process
        time.sleep(1)
        self.axis0.controller.config.vel_gain = 0.0002
        self.axis1.controller.config.vel_gain = 0.0002
        self.axis2.controller.config.vel_gain = 0.0002
        time.sleep(0.5)


        #set motors to velocity control mode
        self.axis0.controller.config.control_mode =CTRL_MODE_VELOCITY_CONTROL
        self.axis1.controller.config.control_mode =CTRL_MODE_VELOCITY_CONTROL
        self.axis2.controller.config.control_mode =CTRL_MODE_VELOCITY_CONTROL
        #rotate CW
        time.sleep(0.5)         
        self.axis0.controller.vel_setpoint = 10000
        self.axis1.controller.vel_setpoint = 10000
        self.axis2.controller.vel_setpoint = 10000
        
        print "searching home position"
        time.sleep(1)
        #just some flags to check later
        axis0_homed =False
        axis1_homed =False
        axis2_homed =False
        #monitor motor currents to check for contact with the end limit
        
        while(not(axis0_homed and axis1_homed and axis2_homed)):
            if( abs(self.axis0.motor.current_control.Iq_measured)>_HOMING_CURRENT_THRESHOLD and not(axis0_homed)):
                self.axis0.controller.vel_setpoint = 0
                self.axis0.controller.vel_setpoint = 0
                axis0_homed = True
                print "axis 0 homed"
            if( abs(self.axis1.motor.current_control.Iq_measured)>_HOMING_CURRENT_THRESHOLD and not(axis1_homed)):
                self.axis1.controller.vel_setpoint = 0
                self.axis1.controller.vel_setpoint = 0
                axis1_homed = True
                print "axis 1 homed"
            if( abs(self.axis2.motor.current_control.Iq_measured)>_HOMING_CURRENT_THRESHOLD and not(axis2_homed)):
                self.axis2.controller.vel_setpoint = 0
                self.axis2.controller.vel_setpoint = 0
                axis2_homed = True
                print "axis 2 homed" 
            time.sleep(0.01)

        time.sleep(1)
        print "Homing complete"
        self.axis0_homepos= self.axis0.encoder.pos_estimate
        self.axis1_homepos= self.axis1.encoder.pos_estimate
        self.axis2_homepos= self.axis2.encoder.pos_estimate
        print "Homing position set" , self.axis0_homepos, self.axis1_homepos, self.axis2_homepos
        time.sleep(1)
        self.axis0.controller.pos_setpoint = self.axis0_homepos
        self.axis1.controller.pos_setpoint = self.axis1_homepos
        self.axis2.controller.pos_setpoint = self.axis2_homepos
        print "switching to position control mode"
        time.sleep(0.5)
        self.axis0.controller.config.control_mode =CTRL_MODE_POSITION_CONTROL
        self.axis1.controller.config.control_mode =CTRL_MODE_POSITION_CONTROL
        self.axis2.controller.config.control_mode =CTRL_MODE_POSITION_CONTROL
        time.sleep(0.5)
        self.axis0.controller.config.vel_gain = 0.000015
        self.axis1.controller.config.vel_gain = 0.000015
        self.axis2.controller.config.vel_gain = 0.000015
        self.axis0.controller.config.pos_gain = 50
        self.axis1.controller.config.pos_gain = 50
        self.axis2.controller.config.pos_gain = 50

        print "odrives are ready"
        self.isReady = True
        
 
    def getJointPos(self):
        '''
        Returns an array of the current joint positions in radians
        '''
        return[-1*(self.axis0.encoder.pos_estimate - self.axis0_homepos)*CPR2RAD,-1*(self.axis1.encoder.pos_estimate - self.axis1_homepos)*CPR2RAD,-1*(self.axis2.encoder.pos_estimate - self.axis2_homepos)*CPR2RAD]

    def setJointPos(self,posval):
        '''
        Set the joint position of three motors, argument is a list of angle values in radians
        NOTE: this function is non blocking, it does not wait for the motors to reach the requested position,
              for that, use the setJointPosWait function
        '''
        #check whether all values are inside limit
        if((0<=posval[0]<=_MAXPOS_LIMIT) and (0<=posval[0]<=_MAXPOS_LIMIT) and (0<=posval[0]<=_MAXPOS_LIMIT)): 
            #print "setpos called", (posval[0]*CPR )/ (2* math.pi) + axis0_homepos,(posval[1]*CPR )/ (2* math.pi) + axis1_homepos,(posval[2]*CPR )/ (2* math.pi) + axis2_homepos
            self.axis0.controller.pos_setpoint = int((-1*posval[0]*CPR )/ (2* math.pi) + self.axis0_homepos)
            self.axis1.controller.pos_setpoint = int((-1*posval[1]*CPR )/ (2* math.pi) + self.axis1_homepos)
            self.axis2.controller.pos_setpoint = int((-1*posval[2]*CPR )/ (2* math.pi) + self.axis2_homepos)
            return True
        else:
            print " commanded motor position out of safe limit"
            return False

    def setJointPosWait(self,posval):
        '''
        Use this function to move to a position. 
        '''
        retval=self.setJointPos(posval)
        curpos = self.getJointPos()
        if retval == True:
            while((abs(posval[0]-curpos[0])>_POS_ERR_THRES) or (abs(posval[1]-curpos[1])>_POS_ERR_THRES) or (abs(posval[2]-curpos[2])>_POS_ERR_THRES) ):
                time.sleep(0.01)
                curpos = self.getJointPos()
        return retval 

