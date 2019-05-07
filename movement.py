from pneumatics import send_pump_cmd

def move_to_location(current_pos,desired_pos,piggy_o,ds):
    desired_thetas=ds.ik(desired_pos)
    piggy_o.setJointPosWait(desired_thetas)
    return

def drop_topping(current_pos,piggy_o,ser,ds):
    '''
    if the current code isnt accurate enough we can lower down first then relase the topping
    '''
    blow_time=2
    send_pump_cmd(2,ser) #blow to release
    sleep(blow_time)
    send_pump_cmd(3,ser) #hold after done blowing

def pick_up_topping(current_pos,piggy_o,ser,z_dist,ds):
    '''
    moves down z_dist amount to pick up topping
    '''
    #change these to set blowing and suck parameters
    blow_time=1
    suck_time=4

    current_thetas=ds.ik(current_pos)
    final_pos=current_pos
    final_pos[2]-=z_dist #move down by z
    final_thetas=ds.ik(final_pos)

    send_pump_cmd(2,ser) #blow first
    sleep(blow_time)
    send_pump_cmd(3,ser) #hold
    piggy_o.setJointPosWait(final_thetas)
    send_pump_cmd(1,ser) #suck
    sleep(suck_time)
    send_pump_cmd(3,ser) #back to hold
    piggy_o.setJointPosWait(current_thetas)
    return
