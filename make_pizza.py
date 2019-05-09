#!/usr/bin/python
from toppings import item, pizza_item
import numpy as np
from camera_trans import toppings_converter,camera_to_robot_list,camera_to_robot_pizza

from selector_help import get_dist_list, get_center_dist, get_available_holes_toppings
from movement import drop_topping, pick_up_topping
from time import sleep
#ok this will be main code that will be referenced for main.py in terms of making the pizza

def add_toppings(dr,ser,camera):
    '''
    continues to add toppings
    '''
    #sleep(10)
    topping_z_offset=100 #mm how far away from toppings we want to be moving
    gripper_height = 60 # mm height of the gripper
    dropping_z_offset = 75 # dropping height

    out_of_the_way_pos=[-290,300,-550] #mm,
    out_way_inter=[0,0,-500]
    dr.moveXYZ(out_way_inter)
    current_pos=out_way_inter
    while True:
        dr.moveXYZ_waypoints(current_pos,out_of_the_way_pos,1)
        current_pos=out_of_the_way_pos
        print "moved to out of the way" # moves robot out of way to take pic
        items_dict=camera.find_toppings() #from jays code we get a dict of all the objects
        print "pic taken"
        print(items_dict)
        print "****************!!!!!!"
        #items_dict['pizza_outers']=[0,0,-600]
       # items_dict['red_cirs']=[[-150,100,-600]]
       # items_dict['yellow_triangles']=[[-50,0,-600]]
       # items_dict['pizza_inners']=[[-100, -50,-600],[-100,-100,-600]]
        try:
            toppings,pizza=toppings_converter(items_dict)
        except:
            print "no pizza found, trying again!"
            continue
        camera_to_robot_list(toppings)
        camera_to_robot_pizza(pizza)
        topping,hole=topping_and_hole_selector(toppings,pizza)
        #topping=item([0,200,-500],'pep')
        #hole=item([200,0,-500],'hole')
        if (topping and hole): #if we have a hole and topping selected
            print "going to pickup"
            print topping.name
            print topping.pos
            #sleep(5)
            topping_loc=topping.pos[::]
            hole_loc=hole.pos[::]
            topping_loc[2]+=(topping_z_offset+gripper_height)

            hole_loc[2]+=(topping_z_offset + gripper_height)

            dr.moveXYZ_waypoints(out_of_the_way_pos,topping_loc,1)
            pick_up_topping(topping_loc,dr,ser,topping_z_offset)
            dr.moveXYZ_waypoints(topping_loc,hole_loc,1)
            drop_topping(hole_loc,dr,ser, dropping_z_offset)
            current_pos=hole_loc
        else:
            print("Ending add_toppings() because no more holes or no more toppings")
            dr.moveXYZ_waypoints(current_pos,out_of_the_way_pos,1)
            return()


def add_shaker(dr,ser):
    '''
        image=capture_image()
        shaker=get_shaker(image)
        pizza=get_pizza(image)
        shaker=camera_to_robot(shaker)
        pizza=camera_to_robot(pizza)
        #plan movement and move and pickup shaker and shake()
    '''
    return()

def topping_and_hole_selector(toppings,pizza):
    '''
    returns topping and hole so that we can add to the pizza
    '''

    good_topping=False #the topping we want to pick up
    good_hole=False
    avail_toppings,avail_holes=get_available_holes_toppings(toppings,pizza)
    #print('available toppings: ', avail_toppings)
    #for now, just select the first available topping and the first available hole
    try:
        good_topping=avail_toppings[0]
        good_hole=avail_holes[0]
    except: #if holes are filled, avail_holes=[], if no toppings,avail_toppings=[] so this deals with that
        print("No more good toppings or holes!")

    return(good_topping,good_hole)