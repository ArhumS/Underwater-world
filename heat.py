import cv2
import numpy as np
from matplotlib import pyplot as plt

# Create blended heat map with JET colormap 

im_map = cv2.imread('left.200.ppm')
im_cloud =cv2.imread('Difference_200.png',0)

def create_heatmap(im_map, im_cloud, kernel_size=(5,5),colormap=cv2.COLORMAP_JET,a1=0.5,a2=0.5):
    '''
    img is numpy array
    kernel_size must be odd ie. (5,5)
    '''
    # create blur image, kernel must be an odd number
    im_cloud_blur = cv2.GaussianBlur(im_cloud,kernel_size,0)

    # Convert back to BGR for cv2
    im_cloud_blur = cv2.cvtColor(im_cloud,cv2.COLOR_GRAY2BGR)
    
    # Apply colormap
    im_cloud_clr = cv2.applyColorMap(im_cloud_blur, colormap)

    # blend images 50/50
    return (a1*im_map + a2*im_cloud_clr).astype(np.uint8) 
    
    # Normalize cloud image?
im_heatmap = create_heatmap(im_map, im_cloud, a1=.5, a2=.5)
cv2.imwrite('colour_diff_d_200.png',im_heatmap)
cv2.imshow('cloud cover',im_heatmap)
cv2.waitKey(5000)


