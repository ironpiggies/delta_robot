#!/usr/bin/python

import numpy as np

from selector_help import get_dist_list, get_center_dist, get_available_holes_toppings
from movement import drop_topping, pick_up_topping
from time import sleep
#ok this will be main code that will be referenced for main.py in terms of making the pizza

def add_toppings(dr,ser,camera):
    '''
    continues to add toppings
    '''
    topping_z_offset=100 #mm how far away from toppings we want to be moving

    out_of_the_way_pos=[0,0,-500] #mm, not sure what this will be

    while True:
        dr.moveXYZ(out_of_the_way_pos)
        print "moved to out of the way" # moves robot out of way to take pic
        items_dict=camera.find_toppings() #from jays code we get a dict of all the objects
        print "pic taken"
        print(items_dict)
        toppings,pizza=toppings_converter(items_dict)
        print toppings, pizza
        toppings=camera_to_robot_list(toppings)
        pizza=camera_to_robot_dict(pizza)
        print toppings,pizza
        topping,hole=topping_and_hole_selector(toppings,pizza)
        topping={"name":"pep","x":0,"y":200,"z":-500,}
        hole={"x":200,"y":0,"z":-500,}
        if (topping and hole): #if we have a hole and topping selected
            print "starting move"
            topping_loc=[topping["x"],topping["y"],topping["z"]+topping_z_offset]
            hole_loc=[hole["x"],hole["y"],hole["z"]+topping_z_offset]

            dr.moveXYZ(topping_loc)
            pick_up_topping(topping_loc,dr,ser,topping_z_offset)
            dr.moveXYZ(hole_loc)
            drop_topping(hole_loc,dr,ser)
        else:
            print("Ending add_toppings() because no more holes or no more toppings")
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

    #for now, just select the first available topping and the first available hole
    try:
        good_topping=avail_toppings[0]
        good_hole=avail_holes[0]
    except: #if holes are filled, avail_holes=[], if no toppings,avail_toppings=[] so this deals with that
        print("No more good toppings or holes!")

    return(good_topping,good_hole)

def camera_to_robot_dict(dict):
    try:
        rotate=np.array([[-1,0,0],[0,-1,0],[0,0,1]]) #180 degree rotation about x
        translate=np.array([[-265],[0],[0]]) #26.5 cenitmeters in negative x

        new_pizza={}
        new_holes=[]
        for hole in dict["holes"]:
            hole_coords=[hole["x"],hole["y"],hole["z"]]
            hole_coords_new=np.add(np.dot(rotate,hole_coords),translate)
            new_holes.append(hole_coords_new)

            pizza_coords=dict["pizza"]
            pizza_coords_new=np.add(np.dot(rotate,pizza_coords),translate)
            new_pizza["holes"]=new_holes
            new_pizza["pizza"]=pizza_coords_new
            return new_pizza
    except:
        print("no pizza detected!")
        return {"holes":[],"pizza":[],}

def camera_to_robot_list(item_list): #update
    '''
    takes a 3x1 position vector and outputs a position relative to the robots frame
    '''
    new_list=[]
    rotate=np.array([[-1,0,0],[0,-1,0],[0,0,1]]) #180 degree rotation about x
    translate=np.array([[-265],[0],[0]]) #26.5 cenitmeters in negative x
    for item in item_list:
        out=item
        coords=[item["x"],item["y"],item["z"]]

        out_coords=np.add(np.dot(rotate,coords),translate)
        out["x"]=out_coords[0]
        out["y"]=out_coords[1]
        out["z"]=out_coords[2]
        new_list.append(out)

    return (new_list)

def toppings_converter(items_dict): #im lazy so instead of rewriting everything ill just convert from jay's item output to the one i want :P
    #update
    topping_list=[]
    hole_list=[]
    pizza={}
    for pep in items_dict['red_cirs']: #exact key might change
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
    for pine in items_dict['yellow_triangles']:
        topping={
        "name":"pineapple",
        "x":pine[0],
        "y":pine[1],
        "z":pine[2],
        }
        topping_list.append(topping)
    for oli in items_dict['black_rings']:
        topping={
        "name":"olive",
        "x":oli[0],
        "y":oli[1],
        "z":oli[2],
        }
        topping_list.append(topping)
    for anch in items_dict['blue_fishes']:
        topping={
        "name":"anchovy",
        "x":anch[0],
        "y":anch[1],
        "z":anch[2],
        }
        topping_list.append(topping)
    for hole in items_dict['pizza_inners']:
        temp_hole={
        "name":"hole",
        "x":hole[0],
        "y":hole[1],
        "z":hole[2],
        }
        hole_list.append(temp_hole)
    pizza={}
    pizza["pizza"]=items_dict["pizza_outers"]
    pizza["holes"]=hole_list #should have x,y,z coordinates and radius
    return topping_list,pizza
