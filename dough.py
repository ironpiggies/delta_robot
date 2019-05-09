from movement import pick_up_topping,drop_topping
from time import sleep
import math
import numpy as np
import sys
sys.path.append('modules/')
from chef2 import get_dough

def mash(dr,ser,camera):
    '''

    :param dr: deltarobot
    :param ser: serial connection to arduino
    :param camera: camera
    :return:

    should look in camera for play dough and masher tool.
    when it sees masher tool it should pick it up and mash the dough.
    '''
    dough_z=-700

    out_of_the_way_pos=[-290,300,-550] #mm,
    dr.moveXYZ(out_of_the_way_pos)
    camera.pipe.stop()
    while True:
        dough_camera=get_dough()  # write new function here. is a np array
        try:
            dough_camera.append(-dough_z)

            rotate = np.array([[1, 0, 0],
                               [0, -1, 0],
                               [0, 0, -1]])  # 180 degree rotation about x
            translate = np.array([190, -20, 0])  # 26.5 cenitmeters in negative x
            dough_out=np.add(np.matmul(np.array(dough_camera),rotate),translate) #transform coordinates to robot frame
            print 'found the stuff, gonna wait now'
            sleep(5) #so ta's can leave
            break
        except:
            print "didn't see playdough, or masher"
            continue

    z_offset=70

    random_pos=[-290,300,dough_z]

    dough_pos=[dough_out[0],dough_out[1],dough_z]
    dough_pos_offset=[dough_out[0],dough_out[1],dough_z+z_offset]
    print dough_pos

    dr.moveXYZ_waypoints(out_of_the_way_pos,random_pos,1)
    pick_up_topping(random_pos,dr,ser,z_offset-70)
    dr.moveXYZ_waypoints(random_pos,dough_pos_offset,1)
    sleep(.1)
    final_pos=smash(dr,dough_pos_offset,dough_pos,z_offset)

    dr.moveXYZ_waypoints(final_pos,out_of_the_way_pos,1)
    drop_topping(out_of_the_way_pos,dr,ser,0)

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
        points.append([x,y,dough_pos[2]]) #add all points in a circle

    current_pos=start_pos[::]
    for point in points:
        #SMASH
        point_offset=point[::]
        point_offset[2]+=z_offset
        dr.moveXYZ_waypoints(current_pos,point_offset,1)
        sleep(0.1)
        dr.moveXYZ_waypoints(point_offset,point,1)
        sleep(0.1)
        dr.moveXYZ_waypoints(point,point_offset,1)#currently at point offset)
        sleep(0.1)
        current_pos=point_offset[::]
    return current_pos
