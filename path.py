import math
import numpy as np

'''
Code for getting many points and planning the path between points
'''

def points_between(start,end,step_size=1): #step_size is in mm
    #return list of points between start and end point along a line by step_sizes
    xstart,ystart,zstart=start[::]
    xend,yend,zend=end[::]
    #print xstart,ystart,zstart
    points=[]
    dist=math.sqrt((xstart-xend)**2+(ystart-yend)**2+(zstart-zend)**2)
    num_points=int(math.ceil((dist)/step_size))
    '''
    xslope=(xend-xstart)/num_points
    yslope=(yend-ystart)/num_points
    zslope=(zend-zstart)/num_points
    #print xslope,yslope,zslope

    #print "********"
    for pt in range(num_points): #might have to add or subtract points to get correct number
        #print(pt)
        x=xstart+pt*xslope
        y=ystart+pt*yslope
        z=zstart+pt*zslope
        #print x,y,z
        points.append([x,y,z])
    '''
    #points=[]
    xpts=np.linspace(xstart,xend,num=num_points).tolist()
    ypts=np.linspace(ystart,yend,num=num_points).tolist()
    zpts=np.linspace(zstart,zend,num=num_points).tolist()
    for pt in range(num_points):
        points.append([xpts[pt],ypts[pt],zpts[pt]])

    return points


