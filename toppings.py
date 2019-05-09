
import numpy as np

class item:
    def __init__(self,pos_list,name):
        self.name=name
        self.pos=pos_list
    def convert(self):
        rotate = np.array([[1, 0, 0],
                           [0, -1, 0],
                           [0, 0, -1]])  # 180 degree rotation about x
        translate = np.array([190, -20, -40])  # 26.5 cenitmeters in negative x
        arr=np.array(self.pos)
        new_arr=np.add(np.matmul(arr,rotate),translate)
        self.pos=new_arr.tolist()

        height=-752

        if self.name=='hole':
            self.pos[2]=height+20
        elif self.name=='fish':
            self.pos[2]=height-3
        else:
            self.pos[2]=height


class pizza_item(item):
    def __init__(self,pos_list,hole_list):
        item.__init__(self,pos_list,'pizza')
        self.holes=hole_list
