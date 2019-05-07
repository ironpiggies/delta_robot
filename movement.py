from pneumatics import send_pump_cmd

def drop_topping(current_pos,dr,ser):
    '''
    if the current code isnt accurate enough we can lower down first then relase the topping
    '''
    blow_time=2
    send_pump_cmd(2,ser) #blow to release
    sleep(blow_time)
    send_pump_cmd(3,ser) #hold after done blowing

def pick_up_topping(current_pos,dr,ser,z_dist):
    '''
    moves down z_dist amount to pick up topping
    '''
    #change these to set blowing and suck parameters
    blow_time=1
    suck_time=4

    final_pos=current_pos
    final_pos[2]-=z_dist #move down by z

    send_pump_cmd(2,ser) #blow first
    sleep(blow_time)
    send_pump_cmd(3,ser) #hold
    dr.moveXYZ(final_pos) #move down
    send_pump_cmd(1,ser) #suck
    sleep(suck_time)
    send_pump_cmd(3,ser) #back to hold
    dr.moveXYZ(current_pos) #move back up
    return
