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
 
if __name__ == '__main__': 
  if len(sys.argv) != 6: 
    print "usage stereoMatch: left right pcd-file disp-file features-file" 
    sys.exit(0) 

  print 'loading images...' 
  imgL = cv2.imread(sys.argv[1]) 
  imgR = cv2.imread(sys.argv[2]) 
 
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
     
  print 'generating 3d point cloud...', 

# Q is a 4x4 disparity-to-depth matrix
  qraw = cv2.cv.Load("Q.xml") 
  Q = np.float32(qraw)
# roi is floating x,y version of an image 
  roi = np.float32(cv2.cv.Load("roi.xml")) 
  region = (roi[0][0], roi[0][1], roi[0][2], roi[0][3]) 
# 2D to 3D reprojection
  points = cv2.reprojectImageTo3D(disp, Q) 
  min = disp.min() 
  cloud = [] 
  size = cv2.cv.GetSize(cv2.cv.fromarray(imgL))
# x,y,z,r,g,b cloud function
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
  with open(sys.argv[3], 'w') as f: 
    f.write(pcd_header % (len(cloud),len(cloud))) 
    np.savetxt(f, cloud, '%f %f %f %f') 
    f.close() 
# formulating & returning a disparity image
  dd = (disp-min_disp)/num_disp
  cv2.cv.SaveImage(sys.argv[4], cv2.cv.fromarray(dd))
  if debug : 
    cv2.imshow('left', imgL) 
    cv2.imshow('disparity', dd)
    cv2.waitKey() 

  print 'generating egomotion cloud'
  grey = cv2.cv.CreateImage(size, 8, 1)
  cv2.cv.CvtColor(cv2.cv.fromarray(imgL), grey, cv2.cv.CV_BGR2GRAY)
  eig = cv2.cv.CreateImage(size, 32, 1)
  temp = cv2.cv.CreateImage(size, 32, 1)
  features = cv2.cv.GoodFeaturesToTrack(grey, eig, temp,
                                        500, 0.01, 10, None, 3, 0, 0.04)
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
  with open(sys.argv[5], 'w') as f: 
    f.write(pcd_header % (len(cloud),len(cloud))) 
    np.savetxt(f, cloud, '%f %f %f %f') 
    f.close() 

