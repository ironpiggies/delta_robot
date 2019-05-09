from movement import pick_up_topping
from time import sleep
import math
import numpy as np

def mash(dr,ser,camera):
    '''

    :param dr: deltarobot
    :param ser: serial connection to arduino
    :param camera: camera
    :return:

    should look in camera for play dough and masher tool.
    when it sees masher tool it should pick it up and mash the dough.
    '''
    out_of_the_way_pos=[-290,300,-550] #mm,
    dr.moveXYZ(out_of_the_way_pos)
    while True:
        #items_dict = camera.find_toppings()  # write new function here
        try:
            #convert somehow
            print 'found the stuff, gonna wait now'
            sleep(5) #so ta's can leave
            break
        except:
            print "didn't see playdough, or masher"
            continue

    z_offset=70
    masher_z=-680
    dough_z=-680

    masher_pos=[-100,-100,masher_z]
    masher_pos_offset=[-100,-100,masher_z+z_offset]

    dough_pos=[0,0,dough_z]
    dough_pos_offset=[0,0,dough_z+z_offset]

    dr.moveXYZ_waypoints(out_of_the_way_pos,masher_pos_offset,1)
    pick_up_topping(dr,ser,z_offset)
    dr.moveXYZ_waypoints(masher_pos_offset,dough_pos_offset,1)
    sleep(.1)
    final_pos=smash(dr,dough_pos,z_offset)
    dr.moveXYZ_waypoints(final_pos,out_of_the_way_pos,1)

def smash(dr,start_pos,dough_pos,z_offset):
    '''

    :param dr:
    :param dough_pos:
    :param z_offset:
    :return:
    move in a circle and smash the whole thing
    '''

    radius=30#mm
    num_points=6 #number of points around the circle
    angles=np.linspace(0,2*math.pi,num=num_points).tolist()
    points=[]
    middle=dough_pos[::]
    points.append(middle)
    for angle in angles:
        x=dough_pos[0]+radius*math.cos(angle)
        y=dough_pos[1]+radius*math.sin(angle)
        points.append[x,y,dough_pos[2]] #add all points in a circle

    current_pos=start_pos[::]
    for point in points:
        #SMASH
        point_offset=point[::]
        point_offset[2]+=z_offset
        dr.moveXYZ_waypoints(current_pos,point_offset,1)
        sleep(0.1)
        dr.moveXYZ_waypoints(point_offset,point,1)
        sleep(0.1)
        dr.move(point,point_offset,1)#currently at point offset)
        sleep(0.1)
        current_pos=point_offset[::]
    return current_pos