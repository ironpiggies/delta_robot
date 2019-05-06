'''
for use in selecting the right toppings and holes
'''

import numpy as np

def get_center_dist(topping1,topping2):
    xdiff=topping1["x"]-topping2["x"]
    ydiff=topping1["y"]-topping2["y"] #not sure if topping is a dictionary or class or what

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
