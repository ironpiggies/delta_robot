#!/usr/bin/python

#ok this will be main code that will be referenced for main.py in terms of making the pizza
'''
here is what needs to happen:
#while True:
#move arms out of the way (can this even be done?)
#capture image
#toppings=color_code.get_all_toppings(image)
#pizza=color_code.get_pizza(image) #gives pizza location and holes to place toppings into
#turn pizza coordinates and toppings coordinates into x,y,z relative to the robot, not the camera
#chosen_hole=hole_selector(toppings,pizza)#check to make sure no toppings in the hole we want to place in
#top=topping_selector(toppings,pizza) #select based on criteria so that we don't choose toppings that are too close to pizza or other toppings
#use iksolver to change top from x,y,z to theta1, theta2, theta3 coordinates so we can use with o drive (does this happen before or after path planning? maybe we do this too all the waypoints we pick? right before we send them to the odrives?)
#path_to_topping=get_path(current_loc,top) #gives path from current position to where we want to do topping things. maybe this isnt really necessary
#path_to_drop=get_path(top,chosen_hole)
#move_along_path(path_to_topping) #only move on when we have the go ahead form the odrives
#start_pickup_sequence() #this involves changing z position, blowing up baloon, force control to lower on topping and suction to grab it, then raising back up (keeping suction)
#move_along_path(path_to_drop)
#start_drop_sequence() #should just be releasing suction and/or blowing out
#end while loop :P
'''

'''
ok: here are the specific functions that we need and progress on them:

capture_image() - needs to capture an image from the camera. should output a numpy array of an image. this could be in a separate file and imported
get_all_toppings(image) - returns locations of toppings. input is numpy array image. currently under construction in color_code.py
get_pizza(image) - returns locations of holes on pizza and location of pizza. will be in color_code.py and will have to be imported
camera_to_robot(items) - returns transformed locations of items by applying rotation matrix and translation to transfrom coordinate frame from camera to robot
hole_selector(toppings,pizza) - returns location of specific hole we want to place a topping into based on which holes are full. if all of the holes are full then we should stop putting toppings on and move on
topping_selector(toppings,pizza) - returns location of the specific topping we want to pick up. based on location to other toppings and to the pizza
#not sure after this about path planning what needs to happen. will discuss with other people.
'''

def add_toppings():
    '''

    '''
    while True:
        '''
        image=capture_image() #also moves arms out of the way?
        toppings=get_all_toppings(image)
        pizza=get_pizza(image)
        toppings=camera_to_robot(toppings)
        pizza=camera_to_robot(pizza)
        hole=hole_selector(toppings,pizza)
        if !hole:
            break #break out of the while loop
        topping=topping_selector(toppings,pizza)
        #now we plan movement and move and pickup and drop off
        '''
    return()

def add_shaker():
    '''
        image=capture_image()
        shaker=get_shaker(image)
        pizza=get_pizza(image)
        shaker=camera_to_robot(shaker)
        pizza=camera_to_robot(pizza)
        #plan movement and move and pickup shaker and shake()
    '''
    return()


def hole_selector(toppings,pizza):
    '''
    returns specific location of hole that we want to put topping into.
    if all holes are taken, return false to allow us to exit out of the while loop.
    check if toppings' x,y position is on or near holes' x,y (or in pizza radius of pizza center)
    to check if the toppings are in the holes. then select a hole that are not filled and return its x,y coordinates
    '''
    return()

def topping_selector(toppings,pizza):
    '''
    returns specific location of a topping we want to pick up. should be some
    minimum radius from other toppings as well as minimum radius from the pizza
    so we don't move the pizza or pick up two toppings
    '''
    return()
