import glob
import random
import cv2
import numpy as np
import argparse

class computeCalibration(object) :
  def __init__(self, filepath) :

  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
  objp = np.zeros((6*7,3), np.float32)
  objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
  objp = objp.reshape(-1,1,3)
  axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
  
  objpoints = []
  imgpoints = []
  
  print "Computing calibration information from " + filepath
  limages=sorted(glob.glob(filepath + '/left.*.ppm'))
  rimages=sorted(glob.glob(filepath + '/right.*.ppm'))
  
  length_l=len(limages)
  length_r=len(rimages)
  
  print 'there are ' + str(length_l) + ' left images '
  print 'there are ' + str(length_r) + ' right images '
  
  needed = 10
  good=[]
  while len(good) < needed:
    x=random.randint(0,length_l-1)
    if x in good:
      continue
    print 'trying ' + limages[x]
    img_l = cv2.imread(limages[x])
    img_l[:,:,0] = img_l[:,:,2] # blue from red (why?)
    gray = cv2.cvtColor(img_l,cv2.COLOR_BGR2GRAY)
    ret, corners_l = cv2.findChessboardCorners(gray, (7,6), None)
    print corners_l
    if not ret :
      continue
  
    print 'trying ' + rimages[x]
    img_r = cv2.imread(rimages[x])
    img_r[:,:,0] = img_r[:,:,2] # blue from red (why?)
    gray = cv2.cvtColor(img_r,cv2.COLOR_BGR2GRAY)
    ret, corners_r = cv2.findChessboardCorners(gray, (7,6), None)
    print corners_r
    if not ret :
      continue
    print 'The Pair ' + limages[x] + " " +rimages[x] + " has the right number of calibration pts "
    good.append(x)
    print good
    print len(good)
  if  ret == True:
    objpoints.append(objp)
    cv2.cornerSubPix(gray,corners_l,(11,11),(-1,-1),criteria)
    imgpoints.append(corners_l)
  
    cv2.drawChessboardCorners(img_l, (7,6), corners_l, ret)
    cv2.drawChessboardCorners(img_r, (7,6), corners_r, ret)
    imageln = cv2.resize(img_l, (0,0), None, 0.45, 0.45)
    imagern = cv2.resize(img_r, (0,0), None, 0.45, 0.45)
    numpy_vert = np.vstack((imageln, imagern))
    cv2.imshow('Numpy Horizontal Concat', numpy_vert)
    cv2.waitKey(5000)
  
  ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints , gray.shape[::-1], None, None)
  print "Camera matrix",mtx
  print "Distortion co-efficient", dist
  print "Rotatioanl vectors",rvecs
  print "Translational vector",tvecs
  
  tot_error = 0
  for i in xrange(len(objpoints)):
  	imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
  	error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
  	tot_error += error
  print "Mean Reprojection Error: ", tot_error/len(objpoints)
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='String directory')
    args = parser.parse_args()
    computeCalibration(args.filepath)

