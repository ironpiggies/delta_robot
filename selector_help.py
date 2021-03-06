'''
for use in selecting the right toppings and holes
'''

import numpy as np
from math import sqrt
from inverse_kinematics import deltaSolver,position

def get_center_dist(topping1,topping2):
    pos1=topping1.pos
    pos2=topping2.pos
    xdiff=pos1[0]-pos2[0]
    ydiff=pos1[1]-pos2[1] #not sure if topping is a dictionary or class or what

    dist=sqrt(xdiff**2+ydiff**2) #distance between centers
    return dist

def get_dist_list(topping,topping_list):
    dist_list=[]
    for top in topping_list:
        dist=(get_center_dist(topping,top))
        if dist !=0:
            dist_list.append(dist) #don't append itself because distance is 0

def get_available_holes_toppings(toppings,pizza):
    '''
    returns a different output_pizza that has a list of the types of toppings
    it can pick up and the holes that can accept them

    this is based on what toppings are already on the pizza too

    will make selection a lot easier
    '''
    ds=deltaSolver() #to help check

    hole_radius= 20#in mm

    pizza_offset=50#in mm
    pizza_radius=110 #distance from center of pizza

    topping_radius=10#in mm, min distance between two toppings

    pizza_center=pizza

    toppings_on_pizza=[]
    holes_filled=[]

    toppings_open=[]
    holes_open=[]

    randomize=False

    for topping in toppings:
        for hole in pizza.holes:
            if (get_center_dist(topping,hole)<hole_radius): #topping is in a hole
                holes_filled.append(hole)
                toppings_on_pizza.append(topping.name)

    for topping in toppings:
        if (get_center_dist(topping,pizza_center)>pizza_radius): #if topping is outside of pizza
            topping_pos=position(topping.pos[0],topping.pos[1],topping.pos[2])
            if ds.check_workspace(topping_pos): #if it is in our viable workspace
                dist_list=get_dist_list(topping,toppings)
                #only sees one topping then get_dist_list returns None
                if (not dist_list or min(dist_list)>topping_radius): #if topping is far enough away from other toppings
                    if len(toppings_on_pizza)<5: #if not all types of toppings are on yet. I think there are 5 diff types of toppings
                        if (topping.name not in toppings_on_pizza): #avoid toppings we have already added

                            toppings_open.append(topping)
                            print("A "+topping.name+ " is available for pickup at ("+str(topping.pos[0])+","+str(topping.pos[1])+")") #prints topping name and location
                    else:
                        toppings_open.append(topping) #if all toppings are on, then all toppings are available to put on
                        randomize=True

    for hole in pizza.holes: #now add holes that aren't in holed_filled
        if (hole not in holes_filled):
            holes_open.append(hole)

    print "Toppings on pizza: "
    print toppings_on_pizza #sanity check
    #print holes_open
    #print toppings_open
    return toppings_open,holes_open,randomize
