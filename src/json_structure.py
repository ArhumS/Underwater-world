import glob
import cv2
import sys
import json
import numpy as np

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20,0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

objpoints = []
imgpoints = []

limages=sorted(glob.glob('../sequences/calib3/left*.ppm'))
rimages=sorted(glob.glob('../sequences/calib3/right*.ppm'))
lengthl=len(limages)
lengthr=len(rimages)

if lengthl != lengthr :
  print " Wrong number of images in the two streams " + str(lengthl) + " " + str(lengthr)
  sys.exit(0)
else :
  print "there are " + str(lengthl) + " images in each stream"
goodset = {}
count = 0

for I in range(0 , lengthr) :
  print "Processing image pair" + limages[I] + " " + rimages[I]

  imgl = cv2.imread(limages[I])
  imgl[:,:,0] = imgl[:,:,2]
  grayl = cv2.cvtColor(imgl,cv2.COLOR_BGR2GRAY)
  ret, cornersl = cv2.findChessboardCorners(grayl, (7,6), None)
  if not ret :
    continue

  imgr = cv2.imread(rimages[I])
  imgr[:,:,0] = imgr[:,:,2]
  grayr = cv2.cvtColor(imgr,cv2.COLOR_BGR2GRAY)
  ret, cornersr = cv2.findChessboardCorners(grayr, (7,6), None)
  if not ret :
    continue
 
  print "image pair good"
 

#Resizing imgs,drawing corners and Displaying good sets
 
 
  cv2.cornerSubPix(grayl,cornersl,(11,11),(-1,-1),criteria)
  cv2.cornerSubPix(grayr,cornersr,(11,11),(-1,-1),criteria)

  pts = cornersl
  vl = []
  for z in pts :
    vl.append(str(z[0][0]))
    vl.append(str(z[0][1]))
  pts = cornersr
  vr = []
  for z in pts :
    vr.append(str(z[0][0]))
    vr.append(str(z[0][1]))
  
  pair = {'left' : limages[I], 'right' : rimages[I], 'leftpts' : vl, 'rightpts' : vr}
  goodset['pair' +  str(count)] = pair
  count = count + 1

  cv2.drawChessboardCorners(imgl,(7,6), cornersl, ret)
  cv2.drawChessboardCorners(imgr,(7,6), cornersr, ret)
  tmpl = cv2.resize(imgl ,(0,0) ,None ,0.5, 0.5)
  tmpr = cv2.resize(imgr ,(0,0) ,None ,0.5, 0.5)
 
  numpy_horizontal = np.array(np.hstack ((tmpl,tmpr)))
  cv2.imshow('pair', numpy_horizontal)
  cv2.waitKey(250)

 
with open("pairs.txt","w") as outfile :
   json.dump(goodset, outfile)

   
 
