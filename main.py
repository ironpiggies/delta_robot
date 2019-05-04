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


    return

def deliver_pizza():
    '''
    first we need to tell mobile robot we are ready. then wait for mobile robot
    to tell us that it is ready. then we execute command to push pizza. then tell
    mobile that we've pushed it off
    '''
    print("Starting to deliver_pizza!")

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


    return
