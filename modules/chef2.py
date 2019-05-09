import pyrealsense2 as rs
import numpy as np
import cv2
from chef_vision import apply_hsv_mask,get_average

def denoise(img,size,iters):


    kernel=np.ones((size,size),np.uint8)
    erosion=cv2.erode(img,kernel,iterations=iters)
    dilation=cv2.dilate(erosion,kernel,iterations=iters)
    return dilation

def get_depth(profile, depth_img, x ,y):
    """
    :param depth_img: depth image of shape (h, w)
    :param x: x index
    :param y: y index
    :return: depth at (x, y) in meter
    """
    depth_scale=profile.get_device().first_depth_sensor().get_depth_scale()
    return depth_img[y, x] * depth_scale

def get_xyz(center, depth_frame, depth_img):
        """
        :param center: (x, y) of a topping
        :param depth_frame: depth frame from RealSense
        :param depth_img: depth image of shape (h, w)
        :return: (x, y, z) of its center in millimeters
        """
        h_im, w_im = depth_img.shape
        w_frame = depth_frame.get_width()
        h_frame = depth_frame.get_height()
        x, y = center
        depth_pixel = [int(float(x) / w_im * w_frame), int(float(y) / h_im * h_frame)]
        depth = depth_frame.get_distance(depth_pixel[0], depth_pixel[1])
        depth_intr = depth_frame.profile.as_video_stream_profile().intrinsics
        depth_point = rs.rs2_deproject_pixel_to_point(depth_intr, depth_pixel, depth)

        # meters to millimeters
        depth_point = [x*1000 for x in depth_point]

        return depth_point


def get_slice(img,zmin,zmax):
    return (img<zmax) * (img>zmin)

def x_slice(img,xmax):
    mask = np.zeros(img.shape)
    mask[:,0:xmax] = 1
    return mask

def get_dough():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    profile=pipeline.start(config)

    while True:

            # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        dough_upper=np.array([80,255,120]) #105,100,102
        dough_lower=np.array([40,100,20]) #85, 43

        masher_upper=np.array([45,255,60])
        masher_lower=np.array([25,150,20])

            # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        slice = get_slice(depth_image, -1, 10).astype(np.uint8)

        slice2=x_slice(slice,400)

        color_image = np.asanyarray(color_frame.get_data())
        #cv2.imshow("color",color_image)





        hsv=cv2.cvtColor(color_image,cv2.COLOR_BGR2HSV)

        masked=cv2.inRange(hsv,dough_lower,dough_upper)
        masked2=cv2.inRange(hsv,masher_lower,masher_upper)
        masked3=slice2*masked2
        denoised=denoise(masked,3,2)
        denoised2=denoise(masked3,7,2)


        xscale=290/(433-191) #mm per pixel
        yscale=290/(298-39)
        xtrans=320
        ytrans=240

        return get_average(denoised,xscale,yscale,xtrans,ytrans)
