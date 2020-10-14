import glob
import random
import cv2
import numpy as np
import argparse


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((7*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)
objp = objp.reshape(-1,1,3)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

objpoints = []
imgpoints_l = []
imgpoints_r = []
  
print("Computing calibration information from ")
limages=sorted(glob.glob('left*.jpg'))
rimages=sorted(glob.glob('right*.jpg'))
  
length_l=len(limages)
length_r=len(rimages)
  
print('there are ' + str(length_l) + ' left images ')
print('there are ' + str(length_r) + ' right images ')
  
needed = 20
good=[]
while len(good) < needed:
   x=random.randint(0,length_l-1)
   if x in good:
       continue
   print('trying ' + limages[x])
   img_l = cv2.imread(limages[x])
   img_l[:,:,0] = img_l[:,:,2] # blue from red (why?)
   gray_l= cv2.cvtColor(img_l,cv2.COLOR_BGR2GRAY)
   ret, corners_l = cv2.findChessboardCorners(gray_l, (9,7), None)
   print(corners_l)
   if not ret :
       continue
   
   print('trying ' + rimages[x])
   img_r = cv2.imread(rimages[x])
   img_r[:,:,0] = img_r[:,:,2] # blue from red (why?)
   gray_r = cv2.cvtColor(img_r,cv2.COLOR_BGR2GRAY)
   ret, corners_r = cv2.findChessboardCorners(gray_r, (9,7), None)
   print(corners_r)
   if not ret :
       continue
   print('The Pair ' + limages[x] + " " +rimages[x] + " has the right number of calibration pts ")
   good.append(x)
   print(good)
   print(len(good))
   if  ret == True:
     objpoints.append(objp)
     cv2.cornerSubPix(gray_l,corners_l,(11,11),(-1,-1),criteria)
     imgpoints_l.append(corners_l)
     cv2.cornerSubPix(gray_r,corners_r,(11,11),(-1,-1),criteria)
     imgpoints_r.append(corners_r)
  
     cv2.drawChessboardCorners(img_l, (9,7), corners_l, ret)
     cv2.drawChessboardCorners(img_r, (9,7), corners_r, ret)
     
     imageln = cv2.resize(img_l, (0,0), None, 0.45, 0.45)
     imagern = cv2.resize(img_r, (0,0), None, 0.45, 0.45)
     numpy_vert = np.vstack((imageln, imagern))
     cv2.imshow('Good Pairs ', numpy_vert)
     cv2.waitKey(1000)
     img_shape = gray_l.shape[::-1]

   ret, mtxl, distl, rvecsl, tvecsl = cv2.calibrateCamera(objpoints, imgpoints_l , gray_l.shape[::-1], None, None)
   ret, mtxr, distr, rvecsr, tvecsr = cv2.calibrateCamera(objpoints, imgpoints_r , gray_r.shape[::-1], None, None)

   print("Left Camera matrix",mtxl)
   print("Left Camera distortion co-efficient", distl)
   print("Left Camera Rotatioanl vectors",rvecsl)
   print("Left Camera Translational vector",tvecsl)

   print("Right Camera matrix",mtxr)
   print("Right Camera distortion co-efficient", distr)
   print("Right Camera Rotatioanl vectors",rvecsr)
   print("Right Camera Translational vector",tvecsr)
 
   tot_error = 0
   print("number of points",len(objpoints))
   for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecsl[i], tvecsl[i], mtxl, distl)
    error = cv2.norm(imgpoints_l[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    tot_error += error
   print("Mean Reprojection Error: ", tot_error/len(objpoints))

   #def stereo_calibrate(self, dims):
 
   flags = 0
   flags |= cv2.CALIB_FIX_INTRINSIC
   flags = CALIB_ZERO_DISPARITY
   # flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
   flags |= cv2.CALIB_USE_INTRINSIC_GUESS
   flags |= cv2.CALIB_FIX_FOCAL_LENGTH
   # flags |= cv2.CALIB_FIX_ASPECT_RATIO
   flags |= cv2.CALIB_ZERO_TANGENT_DIST
   flags |= cv2.CALIB_RATIONAL_MODEL
   
   img_shape = gray_l.shape[::-1]
   print("img_size",img_shape)
   stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER +
                                cv2.TERM_CRITERIA_EPS, 100, 1e-5)
   ret, mtxl, distl, mtxr,distr, R, T, E, F = cv2.stereoCalibrate(objpoints, imgpoints_l,
                imgpoints_r, mtxl,distl, mtxr,distr,img_shape, flags=flags,criteria=stereocalib_criteria)
   print('Intrinsic_mtx_1', mtxl)
   print('dist_1', distl)
   print('Intrinsic_mtx_2', mtxr)
   print('dist_2', distr)
   print('R', R)
   print('T', T)
   print('E', E)
   print('F', F)
   
   R1, R2, P1, P2, Q, ROI1, ROI2 = cv2.stereoRectify(mtxl,distl, mtxr, distr, img_shape, R,T,flag=flags)
   print('R1', R1)
   print('Q', Q)
   print('ROI1', ROI1)
   print('ROI2', ROI2)
   

   
