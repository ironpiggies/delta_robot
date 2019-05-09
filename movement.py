from time import sleep

def drop_topping(current_pos,dr,ser,z_dist):
    '''
    '''
    dr.setLowSpeed()
    final_pos = current_pos[::]
    final_pos[2] -= z_dist  # move down by z
    dr.moveXYZ_waypoints(current_pos,final_pos,1)
    blow_time=.35
    ser.send(2) #blow to release
    sleep(blow_time)
    ser.send(3) #hold after done blowing
    dr.moveXYZ_waypoints(final_pos,current_pos,1)

def pick_up_topping(current_pos,dr,ser,z_dist):
    '''
    moves down z_dist amount to pick up topping
    '''
    #change these to set blowing and suck parameters
    dr.setLowSpeed()
    print "picking up"
    blow_time=1
    suck_time=1.5

    final_pos=current_pos[::]
    final_pos[2]-=z_dist #move down by z


    ser.send(2)#blow first
    sleep(blow_time)
    ser.send(3) #hold
    dr.moveXYZ_waypoints(current_pos,final_pos,1) #move down
    ser.send(1) #suck
    sleep(suck_time)
    #ser.send(3) #back to hold
    dr.moveXYZ_waypoints(final_pos,current_pos,1) #move back up
    return
