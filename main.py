#!/usr/bin/python

import make_pizza
import delta_robot
import pneumatics
import push_pizza
import sys
sys.path.append('modules/')
import chef_vision
import dough
from tcp_commander import sendRoboCommand
import time

'''
#three main events need to happen:
#1)put toppings on pizza
#2)put pizza on mobile robot
#3)make dough
#import separarte codes above and then reference them below. Try to keep this
main.py file pretty clean, as it will allow us to debug only one function at a time
'''

#easy enough to comment one out when we don't want to run everything.
arduino_port="/dev/arduino"


print "starting ser"
ser=pneumatics.pneu_ser(arduino_port)
print "starting camera"
camera=chef_vision.ChefVision()
print "starting dr"
dr=delta_robot.deltaBot()
dr.setLowSpeed()
#dr=1

def put_toppings_on(dr,ser,camera):
    '''
    loop:
    first we gather list of toppings and x,y coordinates as well as pizza(and its holes)
    also check to see what is on pizza already
    then we grab one based on some criteria (ones that aren't too close)
    then move to topping location, activate gripper, pick up and move topping
    if we have filled pizza with toppings (and have one of each), end loop
    also do salt and pepper shaker?
    '''
    print("Starting to put toppings on!")


    make_pizza.add_toppings(dr,ser,camera)
    #make_pizza.add_shaker(dr,ser)

    return

def deliver_pizza(dr,ser,camera):
    '''
    first we need to tell mobile robot we are ready. then wait for mobile robot
    to tell us that it is ready. then we execute command to push pizza. then tell
    mobile that we've pushed it off
    '''

    print("Starting to deliver pizza!")
    while True:
        result=sendRoboCommand('waiting')
        if result=='ready':
            print "got response from mobile robot"
            break
        time.sleep(1)

    push_pizza.push(dr,ser,camera)
    time.sleep(0.5)
    print "Telling Mobile Robot that we are ready"
    sendRoboCommand('transfer')


    return


def make_dough(dr,ser,camera):
    '''
    first we need to wait until we see the dough on the table
    then we identify where it is and do force control (or velocity control?) to mash it
    will require pneumatics to be involved as well probably :P
    '''
    print("Starting to make dough!")
    #while !find_dough():
    #   continue
    #(x,y)=find_dough()
    dough.mash(dr,ser,camera)

    return


# for i in range(10):
#     sendRoboCommand('start')
#     time.sleep(0.5)
# put_toppings_on(dr,ser,camera)
dr.shake([0, 0, -600])
# deliver_pizza(dr,ser,camera)
# make_dough(dr,ser,camera)
