#!/usr/bin/python

from serial import Serial
from time import sleep

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
        return True #return true if it works
    except:
        print("Can't send pump command")
        return False #return false if it doesnt work

#below is for testing
#ser=start_serial("/dev/cu.usbmodem1421")
#print(ser)
#if ser:
#    worked=send_pump_cmd(1,ser)
#    print(worked)
#    while True:
#        print(get_pump_state(ser))

#more testing!


#these numbers are a good starting point. suck_time should be for however long we are moving for
blow_sec=1
suck_sec=6
hold_sec=.5
ser=start_serial("/dev/cu.usbmodem1411") #will need to change this port to whatever port we want to work with
sleep(5) #waits for arduino to reset
#print("here")
send_pump_cmd(2,ser)
sleep(blow_sec)
send_pump_cmd(3,ser)
sleep(hold_sec)
send_pump_cmd(1,ser)
sleep(suck_sec)
send_pump_cmd(2,ser)
sleep(blow_sec)
send_pump_cmd(3,ser)
