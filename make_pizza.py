#!/usr/bin/python
from toppings import item, pizza_item
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

    out_of_the_way_pos=[-290,-275,-600] #mm,

    while True:
        dr.moveXYZ(out_of_the_way_pos)
        print "moved to out of the way" # moves robot out of way to take pic
        items_dict=camera.find_toppings() #from jays code we get a dict of all the objects
        print "pic taken"
        print(items_dict)
        print "****************!!!!!!"
        items_dict['pizza_outers']=[0,0,-600]
        items_dict['red_cirs']=[[-150,100,-600]]
        items_dict['yellow_triangles']=[[-50,0,-600]]
        items_dict['pizza_inners']=[[-100, -50,-600],[-100,-100,-600]]
        toppings,pizza=toppings_converter(items_dict)

        camera_to_robot_list(toppings)
        camera_to_robot_pizza(pizza)
        for topping in toppings:
            print topping.pos
        topping,hole=topping_and_hole_selector(toppings,pizza)
        #topping=item([0,200,-500],'pep')
        #hole=item([200,0,-500],'hole')
        if (topping and hole): #if we have a hole and topping selected
            print "starting move"
            topping_loc=topping.pos[::]
            hole_loc=hole.pos[::]
            topping_loc[2]+=topping_z_offset
            hole_loc[2]+=topping_z_offset

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

def camera_to_robot_pizza(pizza):

    pizza.convert()
    camera_to_robot_list(pizza.holes)

def camera_to_robot_list(item_list): #update
    for item in item_list:
        item.convert()

def toppings_converter(items_dict): #im lazy so instead of rewriting everything ill just convert from jay's item output to the one i want :P
    #update
    topping_list=[]
    hole_list=[]
    pizza={}
    for pep in items_dict['red_cirs']: #exact key might change
        topping=item(pep,'pep')
        topping_list.append(topping)
    for ham in items_dict['pink_squares']: #exact key might change
        topping=item(ham,'ham')
        topping_list.append(topping)
    for pine in items_dict['yellow_triangles']:
        topping=item(pine,'pine')
        topping_list.append(topping)
    for oli in items_dict['black_rings']:
        topping=item(oli,'olive')
        topping_list.append(topping)
    for fish in items_dict['blue_fishes']:
        topping=item(fish,'fish')
        topping_list.append(topping)
    for hole in items_dict['pizza_inners']:
        temp_hole=item(hole,'hole')
        hole_list.append(temp_hole)
    pizza=pizza_item(items_dict["pizza_outers"],hole_list)
    return topping_list,pizza
