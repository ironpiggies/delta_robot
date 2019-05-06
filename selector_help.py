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
