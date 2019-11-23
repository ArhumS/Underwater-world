#!/usr/bin/env python 
# Given the necessary calibration parameters, this computes the stereo 
# match. It outputs two things 
# (i) a pcd coloured point cloud file 
# (ii) a set of 'good' points for doing egomotion estimation
#
# Copyright (c) Michael Jenkin, 2012. All rights reserverd.
#

import sys 
import numpy as np 
import cv2 
 
debug = False
 
pcd_header = '''# .PCD v.7 - Point CLoud Data file format 
VERSION .7 
FIELDS x y z rgb 
SIZE 4 4 4 4 
TYPE F F F F 
COUNT 1 1 1 1 
WIDTH %d 
HEIGHT 1 
VIEWPOINT 0 0 0 1 0 0 0 
POINTS %d 
DATA ascii 
''' 
# to tune for near and far disparity, points (x,y) are chosen from left and right stere img. 
# Far (474,94) and (432,91)
# Near(971,364)and (945,358)
# Routine distance formula gave 41.89 ~ 42 pixels for image with caustics and  37.8 ~ 38 pixel for images with no caustic(near)
# and 25.2,23.2 (Far) caustics and no caustics

# Hence d1 = 25<x1<42, d2= 23<x2<38

if __name__ == '__main__': 
  if len(sys.argv) != 1: 
    print "usage stereoMatch: pcd-file disp-file features-file" 
    sys.exit(0) 

  print 'loading images...' 
  imgL = cv2.imread('undist_l.jpg') 
  imgR = cv2.imread('undist_r.jpg') 
 
# disparity range is not tuned at all... 
  window_size = 3 
  min_disp = 16*6 
  num_disp = 16*10 

# Semi Global Block Matching
  stereo = cv2.StereoSGBM(minDisparity = min_disp,  
      numDisparities = num_disp,  
      SADWindowSize = window_size, 
      uniquenessRatio = 10, 
      speckleWindowSize = 100, 
      speckleRange = 32, 
      disp12MaxDiff = 1, 
      P1 = 8*3*window_size**2, 
      P2 = 32*3*window_size**2, 
      fullDP = False 
  ) 
 
  print 'computing disparity...' 
  disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0 
  
  qraw=[[1.00000000e+00, 0.00000000e+00,   0.00000000e+00, -8.83495800e+02],
        [0.00000000e+00, 1.00000000e+00,   0.00000000e+00, -3.87763466e+02], 
        [0.00000000e+00, 0.00000000e+00,   0.00000000e+00,  1.56506081e+03],
        [0.00000000e+00, 0.00000000e+00,   2.63776428e-01, -0.00000000e+00]]
  
  print 'generating 3d point cloud...', 
  #qraw = cv2.Load("Q.xml") 
  Q = np.float32(qraw)
  #roi = np.float32(cv2.Load("roi.xml")) 
  roi = [(43, 15, 1237, 677)]
  region = (roi[0][0], roi[0][1], roi[0][2], roi[0][3]) 
  points = cv2.reprojectImageTo3D(disp, Q) 
  print '\npoints...\n' , points
  min = disp.min() 
  cloud = [] 

  size = cv2.GetSize(cv2.cv.fromarray(imgL))
  for j in range(size[0]) :
    for i in range(size[1]) :
      imgR[i][j][0] = 0
  for j in range(region[0], region[2]) : 
    for i in range(region[1], region[3]) : 
      if disp[i][j] > min :  
        cloud.append([points[i][j][0], points[i][j][1], points[i][j][2], 
                     imgL[i][j][2]*256*256+ imgL[i][j][1]*256 + 
                     imgL[i][j][0]]) 
        imgR[i][j][0] = 1
  with open(sys.argv[1], 'w') as f: 
    f.write(pcd_header % (len(cloud),len(cloud))) 
    np.savetxt(f, cloud, '%f %f %f %f') 
    f.close() 

  dd = (disp-min_disp)/num_disp
  cv2.SaveImage(sys.argv[2], cv2.fromarray(dd))
  if debug : 
    cv2.imshow('left', imgL) 
    cv2.imshow('disparity', dd)
    cv2.waitKey() 

  print 'generating egomotion cloud'
  grey = cv2.CreateImage(size, 8, 1)
  cv2.CvtColor(cv2.fromarray(imgL), grey, cv2.CV_BGR2GRAY)
  eig = cv2.CreateImage(size, 32, 1)
  temp = cv2.CreateImage(size, 32, 1)
  features = cv2.GoodFeaturesToTrack(grey, eig, temp,500, 0.01, 10, None, 3, 0, 0.04)
  print 'before disparity check', len(features)
  good = []
  for pt in features:
    c = int(pt[0])
    r = int(pt[1])
    print r,c
    if imgR[r][c][0] > 0 :
      good.append(pt)
  print 'after disparity check', len(good)
  print good
  cloud = []
  for pt in good:
    j = int(pt[0])
    i = int(pt[1])
    
    if disp[i][j] > min :  
      cloud.append([points[i][j][0], points[i][j][1], points[i][j][2], 
                    imgL[i][j][2]*256*256+ imgL[i][j][1]*256 + 
                    imgL[i][j][0]]) 
  with open(sys.argv[3], 'w') as f: 
    f.write(pcd_header % (len(cloud),len(cloud))) 
    np.savetxt(f, cloud, '%f %f %f %f') 
    f.close() 

