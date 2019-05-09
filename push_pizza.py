from camera_trans import toppings_converter,camera_to_robot_pizza,camera_to_robot_list
from time import sleep

def push(dr,ser,camera):
    '''

    :param dr: deltarobot
    :param ser: serial connection to arduino
    :param camera: camera
    :return:

    this should:
    find pizza
    put gripper in middle
    move in positive y and push it off the table
    broken down: move to pizza center (pushing on it slightly). then move to y=0 line. then push in +y until it is off
    '''

    print "starting to push pizza off"

    out_of_the_way_pos=[-290,300,-550] #mm,

    dr.moveXYZ(out_of_the_way_pos)
    while True:
        items_dict = camera.find_toppings()  # from jays code we get a dict of all the objects
        try:
            toppings,pizza=toppings_converter(items_dict)
            print "found pizza"
            break
        except:
            print "no pizza found, trying again!"
            continue
    camera_to_robot_pizza(pizza)


    pizza_z=-610 #z value for moving the pizza
    z_offset=10 #offset value for moving around
    pizza_x_1=pizza.pos[0]
    pizza_y_1=pizza.pos[1]

    pizza_x_2=0
    pizza_y_2=pizza_y_1

    pizza_x_3=0
    pizza_y_3=300

    pos1_prev=[pizza_x_1,pizza_y_1,pizza_z+z_offset]
    pos1=[pizza_x_1,pizza_y_1,pizza_z]
    pos2=[pizza_x_2,pizza_y_2,pizza_z]
    pos3=[pizza_x_3,pizza_y_3,pizza_z]

    dr.moveXYZ_waypoints(out_of_the_way_pos,pos1_prev,1)
    sleep(.1)
    ser.send(2)
    sleep(.3) #inflate a little
    ser.send(3)
    dr.moveXYZ_waypoints(pos1_prev,pos1,1)
    sleep(.1)
    dr.moveXYZ_waypoints(pos1,pos2,1)
    sleep(.1)
    dr.moveXYZ_waypoints(pos2,pos3,1)
    return