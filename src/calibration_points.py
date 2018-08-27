#
# calibration_points.py - go through a directory of left/right view of
# a calibration target and run the calibration point code on it. This
# code assumes that there is a directory containing files left.n.ppm and
# right.n.ppm which are the raw images. 
#
# Version History
#   v1.0 - preliminary version
#   V2.0 - fancier graphics and now outputs the image shape in the json
#   v2.1 - even fancier graphics
#

import glob
import cv2
import sys
import json
import numpy as np
import argparse

# Default size of calibration grid is 7x6


parser = argparse.ArgumentParser()
parser.add_argument('filepath', help='String directory')
parser.add_argument('output', help='String output filename')
parser.add_argument('--display', type=bool, default=False, help='display checkerboards as processed')
parser.add_argument('--rows', type=int, default=7, help='number of rows in checkerboard')
parser.add_argument('--cols', type=int, default=6, help='number of cols in checkerboard')
args = parser.parse_args()
rows = args.rows
columns = args.cols
print rows, columns

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20,0.001)
objp = np.zeros((columns*rows,3), np.float32)
objp[:,:2] = np.mgrid[0:rows,0:columns].T.reshape(-1,2)

objpoints = []
imgpoints = []

limages=sorted(glob.glob(args.filepath + '/left.*.ppm'))
rimages=sorted(glob.glob(args.filepath + '/right.*.ppm'))
lengthl=len(limages)
lengthr=len(rimages)

if lengthl != lengthr :
  print " Wrong number of images in the two streams " + str(lengthl) + " " + str(lengthr)
  sys.exit(0)
else :
  print "there are " + str(lengthl) + " images in each stream"
goodset = {}
count = 0

for i in range(0 , lengthr) :
  print "Processing image pair" + limages[i] + " " + rimages[i]

  imgl = cv2.imread(limages[i])
  imgl[:,:,0] = imgl[:,:,2]
  grayl = cv2.cvtColor(imgl,cv2.COLOR_BGR2GRAY)
  retl, cornersl = cv2.findChessboardCorners(grayl, (rows,columns), None)
  tmpl = cv2.resize(imgl ,(0,0) ,None ,0.5, 0.5)
  if not retl :
    cv2.putText(tmpl, limages[i] + ' fails', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
  else :
    cv2.cornerSubPix(grayl, cornersl, (11,11), (-1,-1), criteria)
    cv2.putText(tmpl, limages[i] + ' success', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

  imgr = cv2.imread(rimages[i])
  imgr[:,:,0] = imgr[:,:,2]
  grayr = cv2.cvtColor(imgr,cv2.COLOR_BGR2GRAY)
  retr, cornersr = cv2.findChessboardCorners(grayr, (rows,columns), None)
  tmpr = cv2.resize(imgr ,(0,0) ,None ,0.5, 0.5)
  if not retr :
    cv2.putText(tmpr, rimages[i] + ' fails', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
  else :
    cv2.cornerSubPix(grayr, cornersr, (11,11), (-1,-1), criteria)
    cv2.putText(tmpr, rimages[i] + ' success', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

  if args.display :
    nh = np.array(np.hstack((tmpl, tmpr)))
    cv2.imshow('pair', nh)
    cv2.waitKey(250)
 

  if retl and retr :
    print "image pair good"
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
  
    pair = {'left' : limages[i], 'right' : rimages[i], 'leftpts' : vl, 'rightpts' : vr, 'leftshape' : imgl.shape, 'rightshape' : imgr.shape}
    goodset['pair' +  str(count)] = pair
    count = count + 1

 
with open(args.output,"w") as outfile :
   json.dump(goodset, outfile)

   
 
