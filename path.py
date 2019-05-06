import math


'''
Code for getting many points and planning the path between points
'''

def points_between(start,end,step_size=1): #step_size is in mm
    #return list of points between start and end point along a line by step_sizes
    xstart,ystart,zstart=start
    xend,yend,zend=end

    points=[]

    num_points=int(math.ceil((xstart-xend)/step_size))
    xslope=(xend-xstart)/num_points
    yslope=(yend-ystart)/num_points
    zslope=(zend-zstart)/num_points

    for pt in range(num_points): #might have to add or subtract points to get correct number
        print(pt)
        x=xstart+pt*xslope
        y=ystart+pt*yslope
        z=zstart+pt*zslope
        points.append((x,y,z))
    points.append((xend,yend,zend))
    return points


print points_between([100,0,0],[-10,0,0])
