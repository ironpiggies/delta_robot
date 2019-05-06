#!/usr/bin/python
'''
# author achuwils
# This code sets the configuration of the odrive 
# nb: it does not set the motor phase resistance and inductance values
#     The following values are obtained during calibration, which
#     can be used later

02 motor0 (axis0)
axis0 phase resistance 0.3386945426464081
axis0 phase inductance  0.00023896312632132322

02 Motor1 (axis1)
In [6]: odrv0.axis1.motor.config.phase_resistance
Out[6]: 0.3414915204048157
In [5]: odrv0.axis1.motor.config.phase_inductance
Out[5]: 0.0002492110070306808


01 Motor Motor0 (axis2)
In [37]: odrv1.axis0.motor.config.phase_resistance
Out[37]: 0.321752101183
In [38]: odrv1.axis0.motor.config.phase_inductance
Out[38]:  0.000218976492761


'''
import odrive
from odrive.enums import *

import time

#2084378A3548

#old
#usb_serials = ['2087377B3548','2084377A3548']

usb_serials = ['2087377B3548','2084378A3548']
odrvs = [None,None]
axes = [None, None, None]
axis0 = None
axis1 = None
axis2 = None

def connect_all():
    global axis0, axis1, axis2, axes
    for ii in range(len(odrvs)):
        if usb_serials[ii] == None:
            continue
        print("finding odrive: " + usb_serials[ii]+ "...")
        odrvs[ii]= odrive.find_any(serial_number = usb_serials[ii])
        print("found odrive! " + str(ii))
    axis0 = odrvs[0].axis0
    axis1 = odrvs[0].axis1
    axis2 = odrvs[1].axis0
    axes[0] = axis0
    axes[1] = axis1
    axes[2] = axis2
connect_all()



print "configuring axis0"
odrvs[0].config.brake_resistance = 0
axis0.controller.config.vel_limit = 200000
axis0.controller.config.pos_gain = 250
axis0.controller.config.vel_gain = 0.000005
axis0.controller.config.vel_integrator_gain = 0
axis0.motor.config.calibration_current = 4
axis0.motor.config.current_lim = 5.0
axis0.motor.config.pole_pairs = 4
axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
axis0.motor.config.phase_resistance = 0.3386945426464081
axis0.motor.config.phase_inductance = 0.00023896312632132322
axis0.motor.config.pre_calibrated = True
axis0.encoder.config.cpr = 4000
axis0.encoder.config.use_index= True
axis0.encoder.config.zero_count_on_find_idx = True
axis0.encoder.config.idx_search_speed = 1
axis0.encoder.config.pre_calibrated = False
axis0.config.startup_motor_calibration = False
axis0.config.startup_encoder_index_search = True
axis0.config.startup_closed_loop_control =  True
axis0.config.startup_encoder_offset_calibration = True


print "cnfiguring axis1"

axis1.controller.config.vel_limit = 200000
axis1.controller.config.pos_gain = 250
axis1.controller.config.vel_gain = 0.000005
axis1.controller.config.vel_integrator_gain = 0
axis1.motor.config.calibration_current = 4
axis1.motor.config.current_lim = 5.0
axis1.motor.config.pole_pairs = 4
axis1.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
axis1.motor.config.phase_resistance = 0.3414915204048157
axis1.motor.config.phase_inductance = 0.0002492110070306808
axis1.motor.config.pre_calibrated = True
axis1.encoder.config.cpr = 4000
axis1.encoder.config.use_index= True
axis1.encoder.config.zero_count_on_find_idx = True
axis1.encoder.config.idx_search_speed = 1
axis1.encoder.config.pre_calibrated = False
axis1.config.startup_motor_calibration = False
axis1.config.startup_encoder_index_search = True
axis1.config.startup_closed_loop_control =  True
axis1.config.startup_encoder_offset_calibration = True


odrvs[0].save_configuration()
time.sleep(5)

print "configuring axis2"

odrvs[1].config.brake_resistance = 0
axis2.controller.config.vel_limit = 200000
axis2.controller.config.pos_gain = 250
axis2.controller.config.vel_gain = 0.000005
axis2.controller.config.vel_integrator_gain = 0
axis2.motor.config.calibration_current = 4
axis2.motor.config.current_lim = 5.0
axis2.motor.config.pole_pairs = 4
axis2.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
axis2.motor.config.phase_resistance = 0.321752101183
axis2.motor.config.phase_inductance =   0.000218976492761
axis2.motor.config.pre_calibrated = True
axis2.encoder.config.cpr = 4000
axis2.encoder.config.use_index= True
axis2.encoder.config.zero_count_on_find_idx = True
axis2.encoder.config.idx_search_speed = 1
axis2.encoder.config.pre_calibrated = False
axis2.config.startup_motor_calibration = False
axis2.config.startup_encoder_index_search = True
axis2.config.startup_closed_loop_control =  True
axis2.config.startup_encoder_offset_calibration = True


odrvs[1].save_configuration()
time.sleep(5)

print "reboot"
time.sleep(2)
try:
    odrvs[0].reboot()
except:
    print "Rebooting odrive 0"    
try:
    odrvs[1].reboot()
except:
    print "Rebooting odrive 1"    

