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
import numpy as np

from movement import pick_up_topping

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


def move_out_of_way(dr):
    out_of_the_way_pos = [-290, 300, -550]  # mm,
    out_way_inter = [0, 0, -500]
    dr.moveXYZ(out_way_inter)
    current_pos = out_way_inter
    dr.setHighSpeed()
    dr.moveXYZ_waypoints(current_pos, out_of_the_way_pos, 5)

def camera_to_robot_frame(pos):
    """ Convert from camera frame to robot frame
    :param pos: a list, (x, y, z)
    :return: a list, (x, y, z)
    """
    # Coordinate transformation
    pos = np.array(pos)
    rotate = np.array([[1, 0, 0],
                       [0, -1, 0],
                       [0, 0, -1]])  # 180 degree rotation about x
    translate = np.array([190, -20, -40])  # 26.5 cenitmeters in negative x
    pos = np.add(np.matmul(pos, rotate), translate).tolist()
    return pos

def add_pepper(dr, ser, camera):
    move_out_of_way(dr)

    # a list of coordinates
    shakers_pos_in_camera_frame = []
    for _ in range(10): # Try five times
        shakers_pos_in_camera_frame = camera.find_shaker()
        if len(shakers_pos_in_camera_frame) > 0:
            break

    if len(shakers_pos_in_camera_frame) > 0:
        print("shaker found")
        shaker_pos = shakers_pos_in_camera_frame[0]

        shaker_pos = camera_to_robot_frame(shaker_pos)

        print("shaker pos: {}".format(shaker_pos))
        target_pos = shaker_pos
        target_pos[2] = -500
        reply = raw_input("confirm? y/N")
        if reply == "y":
            dr.moveXYZ(target_pos)
            pick_up_topping(current_pos=target_pos, dr=dr, ser=ser, z_dist=130)
            move_out_of_way(dr)
            toppings = camera.find_toppings()
            pizza = toppings["pizza_outers"]
            if len(pizza) > 0:
                print("pizza found")
                pizza = pizza[0]
                pizza = camera_to_robot_frame(pizza)
                print("pizza position: {}".format(pizza))
                target_pos = pizza
                target_pos[2] = -500
                raw_input("looks good? (if not, it's your chance to kill me")
                dr.moveXYZ(target_pos)
                dr.shake(target_pos)
            else:
                print("did not find pizza")
    else:
        print("Did not find shaker")


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


for i in range(10):
    sendRoboCommand('start')
    time.sleep(0.5)
put_toppings_on(dr,ser,camera)

# Not working. Don't run it!!
# add_pepper(dr, ser, camera)

deliver_pizza(dr,ser,camera)
make_dough(dr,ser,camera)
