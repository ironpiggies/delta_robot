#!/usr/bin/python

import numpy as np

from selector_help import get_dist_list, get_center_dist

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
    #while True:
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

def topping_and_hole_selector(toppings,pizza):
    '''
    returns topping and hole so that we can add to the pizza
    '''


    good_topping=False #the topping we want to pick up
    good_hole=False
    avail_toppings,avail_holes=get_available_holes_toppings(toppings,pizza)

    #for now, just select the first available topping and the first available hole
    try:
        good_topping=avail_toppings[0]
        good_hole=avail_holes[0]
    except: #if holes are filled, avail_holes=[], if no toppings,avail_toppings=[] so this deals with that
        print("No more good toppings or holes!")

    return(good_topping,good_hole)

def camera_to_robot(position):
    '''
    takes a 3x1 position vector and outputs a position relative to the robots frame
    '''
    rotate=np.array([[-1,0,0],[0,-1,0],[0,0,1]]) #180 degree rotation about x
    translate=np.array([[-265],[0],[0]]) #26.5 cenitmeters in negative x
    print(rotate)
    print(translate)
    out=np.add(np.dot(rotate,position),translate)
    return (out)

def toppings_converter(items_dict): #im lazy so instead of rewriting everything ill just convert from jay's item output to the one i want :P
    topping_list=[]
    hole_list=[]
    pizza={}
    for pep in items_dict['red_circles']: #exact key might change
        topping={
        "name":"pepperoni",
        "x":pep[0],
        "y":pep[1],
        "z":pep[2],
        }
        topping_list.append(topping)
    for ham in items_dict['pink_squares']: #exact key might change
        topping={
        "name":"ham",
        "x":ham[0],
        "y":ham[1],
        "z":ham[2],
        }
        topping_list.append(topping)
    for pine in items_dict('yellow_triangles'):
        topping={
        "name":"pineapple",
        "x":pine[0],
        "y":pine[1],
        "z":pine[2],
        }
        topping_list.append(topping)
    for oli in items_dict('black_rings'):
        topping={
        "name":"olive",
        "x":oli[0],
        "y":oli[1],
        "z":oli[2],
        }
        topping_list.append(topping)
    for anch in items_dict('blue_fish'):
        topping={
        "name":"anchovy",
        "x":anch[0],
        "y":anch[1],
        "z":anch[2],
        }
        topping_list.append(topping)
    for hole in items_dict('holes'):
        temp_hole={
        "name":"hole",
        "x":hole[0],
        "y":hole[1],
        "z":hole[2],
        }
        hole_list.append(temp_hole)
    pizza=items_dict["pizza"]
    pizza["holes"]=hole_list #should have x,y,z coordinates and radius
    return topping_list,pizza

def get_available_holes_toppings(toppings,pizza):
    '''
    returns a different output_pizza that has a list of the types of toppings
    it can pick up and the holes that can accept them

    this is based on what toppings are already on the pizza too

    will make selection a lot easier
    '''
    hole_radius= 50#in mm

    pizza_offset=50#in mm
    pizza_radius=float(pizza["radius"])+pizza_offset #distance from center of pizza

    topping_radius=50#in mm, min distance between two toppings

    toppings_on_pizza=[]
    holes_filled=[]

    toppings_open=[]
    holes_open=[]

    for topping in toppings:
        for hole in pizza["holes"]:
            if (get_center_dist(topping,hole)<hole_radius): #topping is in a hole
                holes_filled.append(hole)
                toppings_on_pizza.append(topping["name"])

    for topping in toppings:
        if (get_center_dist(topping,pizza)>pizza_radius):   #if topping is outside of pizza
            if min(get_dist_list(topping,toppings))>topping_radius: #if topping is far enough away from other toppings
                if len(toppings_on_pizza)<5: #if not all types of toppings are on yet. I think there are 5 diff types of toppings

                    if (topping["name"] not in toppings_on_pizza): #avoid toppings we have already added
                        toppings_open.append(topping)
                        print("A "+topping["name"]+ "is available for pickup at ("+topping["x"]+","+topping["y"]+")") #prints topping name and location
                else:
                    toppings_open.append(topping) #if all toppings are on, then all toppings are available to put on

    for hole in pizza["holes"]: #now add holes that aren't in holed_filled
        if (hole not in holes_filled):
            holes_open.append(hole)

    print("Toppings on pizza: "+toppings_on_pizza) #sanity check

    return toppings_open,holes_open
