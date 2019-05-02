#!/usr/bin/python

from serial import Serial
import numpy as np

#'/dev/ttyACM0'


def start_serial(port):
    try:
        serialComm = Serial(port, 9600, timeout = 5) #can change number to reflect the baud rate on the arduino
        return serialComm #return this to use in send_pump_cmd and get_pump_state
    except:
        print("Cannot start serial connection!")
        return False

#/pumping is 0 if nothing, 1 if sucking, 2 if blowing, 3 if holding
def send_pump_cmd(pump_cmd,serialComm):
    try:
        str_cmd =  str(pump_cmd) + '\n'
        serialComm.write(str_cmd) #send pump value to arduino
        return True
    except:
        print("Can't send pump command")
        return False

def get_pump_state(serialComm):
    try:
        serialData = serialComm.readline()
        if serialData:
            return True
        else:
            return False
    except:
        print("Didn't read from Arduino")
        return False

#below is for testing
#ser=start_serial("/dev/cu.usbmodem1421")
#print(ser)
#if ser:
#    worked=send_pump_cmd(1,ser)
#    print(worked)
#    while True:
#        print(get_pump_state(ser))
