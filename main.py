#!/usr/bin/python

'''
#three main events need to happen:
#1)put toppings on pizza
#2)put pizza on mobile robot
#3)make dough
#import separarte codes above and then reference them below. Try to keep this
main.py file pretty clean, as it will allow us to debug only one function at a time
'''

#easy enough to comment one out when we don't want to run everything.
put_toppings_on()
deliver_pizza()
make_dough()


def put_toppings_on():
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
    #while True:
    #move arms out of the way (can this even be done?)
    #capture image
    #toppings=color_code.get_all_toppings(image)
    #pizza=color_code.get_pizza(image) #gives pizza location and holes to place toppings into
    #chosen_hole=hole_selector(toppings,pizza)#check to make sure no toppings in the hole we want to place in
    #top=topping_selector(toppings,pizza) #select based on criteria so that we don't choose toppings that are too close to pizza or other toppings
    #path_to_topping=get_path(current_loc,top) #gives path from current position to where we want to do topping things
    #path_to_drop=get_path(top,chosen_hole)
    #move_along_path(path_to_topping) #only move on when we have the go ahead form the odrives
    #start_pickup_sequence() #this involves changing z position, blowing up baloon, force control to lower on topping and suction to grab it, then raising back up (keeping suction)
    #move_along_path(path_to_drop)
    #start_drop_sequence() #should just be releasing suction and/or blowing out
    #end while loop :P
    return

def deliver_pizza():
    '''
    first we need to tell mobile robot we are ready. then wait for mobile robot
    to tell us that it is ready. then we execute command to push pizza. then tell
    mobile that we've pushed it off
    '''
    print("Starting to deliver pizza!")

    #send_pizza_ready_signal() or something
    #while !mobile_in_position():
    #   continue
    #push_pizza_off()
    #send_deliver_signal()

    return

def make_dough():
    '''
    first we need to wait until we see the dough on the table
    then we identify where it is and do force control (or velocity control?) to mash it
    will require pneumatics to be involved as well probably :P
    '''
    print("Starting to make dough!")
    #while !find_dough():
    #   continue
    #(x,y)=find_dough()
    #mash()

    return
