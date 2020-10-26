# -*- coding: utf-8 -*-
import sys
import glob
import numpy
import numpy as np
import cv2
import cv2 as cv
import struct
from matplotlib import pyplot as plt
from PIL import Image

pcd_header = '''# .PCD v.7 - Point Cloud Data file format 
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
print ('loading images...')
imgL = cv2.imread('calibresult_1l_212.png') # no caustics
imgR = cv2.imread('calibresult_1r_212.png')
#imgL = cv2.imread('calibresult_1l.png') #  caustics
#imgR = cv2.imread('calibresult_1r.png')
#imgL = cv2.imread('left.3218.jpg') # with caustics
#imgR = cv2.imread('right.3218.jpg')
#imgL = cv2.imread('l_pin_c.jpg') # with caustics
#imgR = cv2.imread('r_pin_c.jpg')
#imgL = cv2.imread('l_pin_nc.jpg') # no caustics
#imgR = cv2.imread('r_pin_nc.jpg')
imgL = cv2.imread('left.200.png') 
imgR = cv2.imread('right.200.png')

size_imgL = imgL.shape
size_imgR = imgR.shape
print ('img size_L...',size_imgL)
print ('img size_R..',size_imgR)


# disparity range is not tuned at all... 
window_size = 5
min_disp = 5
num_disp = 16*4

# Semi Global Block Matching

stereo = cv2.StereoSGBM_create(minDisparity = min_disp,  
     numDisparities = num_disp,  
     uniquenessRatio = 10, # increased from 7 (less cluttered)15 # change to 50 later
     speckleWindowSize = 200, #from 200,100 -150(less speckle pixels below which a disparity blob is dismissed
     speckleRange = 32, #from 32,no such difference 
     disp12MaxDiff = 1, 
     P1 = 8*3*window_size**2, 
     P2 = 32*3*window_size**2, 
)

print ('computing disparity...')
disp = stereo.compute(imgL, imgR).astype(np.float32)/16
plt.imshow(disp,'gray')
plt.show()

size_disp = disp.shape
print ('image resolution',size_disp)

out_disp = np.array(disp,np.uint8)

# Create an excel file that consists of the points (column, disparity) looping over one scan line for entire columns
scanline = 75
out_col = np.array(disp[scanline,:])

len_out_col = len(out_col)
#print(' disparity colum-wise...',len_out_col)
    
#for a in range(0,len_out_col):
 # if disp[scanline,a] >= min_disp:
#   print(str(disp[scanline,a]))
     
valid = disp >= min_disp
valid_values = np.sum(valid)
print ('valid disparity.....',valid_values)

out_norm = (disp - min_disp) / num_disp
out = 63 + valid * 192 * (disp - min_disp) / num_disp
out = np.array(out,np.uint8)

valid_2 = np.zeros(imgR.shape,dtype = np.uint8)
valid_2[:,:,0]=valid
valid_2[:,:,1]=valid
valid_2[:,:,2]=valid
A = valid_2 * imgR
#print ('A', np.array(A))

red = np.zeros(imgR.shape,dtype = np.uint8)
red[:,:,2]= 144

invalid = disp < min_disp
invalid_val = np.sum(invalid)
print ('invalid disparity.....',invalid_val)

invalid_2 = np.zeros(imgR.shape,dtype = np.uint8)
invalid_2[:,:,0]=invalid
invalid_2[:,:,1]=invalid
invalid_2[:,:,2]=invalid
B = invalid_2 * red
#print ('B',np.array(B))
cv2.imshow('B',B)
cv2.waitKey(5000)
C = A + B
#print ('both_valid and inv',sum(C))
cv2.imshow('out',C)
#cv2.imwrite('C.png',C)
cv2.waitKey(1000)

qraw = np.float32([[1,0,0,0],
                  [0,-1,0,0],
                  [0,0, 11378e-03,0], #Focal length multiplication obtained experimentally. 
                  [0,0,0,1]])
Q = np.float32(qraw)
roi = [(0, 22, 1246, 668)]
region = (roi[0][0], roi[0][1], roi[0][2], roi[0][3]) 

print ('generating points...')
points = cv2.reprojectImageTo3D(disp,Q)
print (points)
min  = disp.min()
print ('min',min)
cloud = []
colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)

for j in range(size_disp[1]): #image width  = 1252
 for i in range(size_disp[0]): #image hgt= 671
    if disp[i][j] > min:
       t= struct.unpack('f',struct.pack('BBBB',imgL[i][j][0],imgL[i][j][1],imgL[i][j][2],70))[0]
       cloud.append([points[i][j][0], points[i][j][1], points[i][j][2], t])
    imgR[i][j][0] = 1
with open('pc_no.pcd', 'w') as f: 
 f.write(pcd_header % (len(cloud),len(cloud))) 
 np.savetxt(f, cloud, '%f %f %f %f') 
 f.close()

print ('generating Egomotion Cloud')
imgLg=cv2.cvtColor(imgL,cv2.COLOR_BGR2GRAY)
features  = cv2.goodFeaturesToTrack(imgLg, 500, 0.01, 10, 3)

print ("features tracked:",features)
print ("points before disparity check,feature length:", len(features))
good = []
for pt in range(len(features)):
   r = int(features[pt][0][1])
   c = int(features[pt][0][0])
   print ('R:',r,'C:',c)
   if np.array(imgL[r][c][0]) > 0:
       good.append(features[pt])
print ("good:\n",good)
print ('points after after disparity check,', len(good))

for pt in range(len(good)):
   i = int(good[pt][0][1])
   j = int(good[pt][0][0])
   if disp[i][j] > min :
      t= struct.unpack('f',struct.pack('BBBB',imgL[i][j][0],imgL[i][j][1],imgL[i][j][2],74))[0]
      cloud.append([points[i][j][0], points[i][j][1], points[i][j][2],t]) 
with open('ego_no.pcd', 'w') as f:
 f.write(pcd_header % (len(cloud),len(cloud)))
 np.savetxt(f, cloud, '%f %f %f %f')
 f.close() 


 
