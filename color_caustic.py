import glob
import cv2
import sys
import math
import numpy as np
img = cv2.imread('left.200.ppm')
cur = cv2.imread('left.200.ppm')
nxt = cv2.imread('left.201.ppm')
#limages=sorted(glob.glob('lefts/left*.ppm'))
#lengthl=len(limages)

#img_width = 720
#img_height = 1280
#diff_max = np.zeros((720,1280))
#diff_min = np.zeros((720,1280))
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img = cv2.bitwise_not(img)
#b,g,r = cv2.split(img)
#z = np.zeros_like(r)
#img = cv2.merge((z,z,r))
#img2 = np.array(img, copy=True)
blur = cv2.GaussianBlur(img,(3,3),0)
ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
white_px = np.asarray([120, 140, 160]) # r g b 208 249 214
black_px = np.asarray([0, 165, 255])

(row, col, _) = img.shape
for r in range(row): # thresholds the img
  for c in range(col):
        if (img[r][c][0] >= white_px[2]) and (img[r][c][1] >= white_px[1]) and (img[r][c][2] >= white_px[0]) :
           img[r][c] = black_px

cv2.imwrite('intensity.png', img)

for r in range(row) :

  for c in range(col) :
    if (cur[r][c][0] - nxt[r][c][0]) > 100 or (cur[r][c][1] - nxt[r][c][1]) > 100 or (cur[r][c][2] - nxt[r][c][2]) > 100 :
      cur[r][c] = black_px

cv2.imwrite('difference.png', cur)

p = cv2.imread('left.200.ppm')
for r in range(row) :
  for c in range(col) :
    if (img[r][c][0] == black_px[0]) and (img[r][c][1] == black_px[1]) and (img[r][c][2] == black_px[2]) and (cur[r][c][0] == black_px[0]) and (cur[r][c][1] == black_px[1]) and (cur[r][c][2] == black_px[2]) :
      p[r][c] = black_px
cv2.imwrite('both.png', p)
  





#for r in xrange(row):
 #   for c in xrange(col):
   # diff_max[x,y]= max([img[1][x,y],img[2][x,y],img[3][x,y],img[4][x,y]])
   # diff_min[x,y]= np.amin(img[1][x,y],img[2][x,y],img[3][x,y],img[4][x,y])
#out_diffx = np.array(diff_max, dtype=np.uint8)
#print(out_diffx)
  
#tmpl = cv2.resize(imgl ,(0,0) ,None ,0.5, 0.5)
#tmpn = cv2.resize(imgn ,(0,0) ,None ,0.5, 0.5)
#tmpd = cv2.resize(diff ,(0,0) ,None ,0.5, 0.5)
#numpy_horizontal = np.array(np.hstack ((tmpl,tmpn,tmpd)))
#cv2.imshow('pair difference', numpy_horizontal)
#cv2.imwrite("result.png",numpy_horizontal )
#cv2.imwrite("Difference.png" , diff)

#img1 = cv2.imread("abs_diff_hh.png")
#img2 = cv2.imread("out_path_or.png")
#diff_b  = cv2.absdiff(img1, img2)
#cv2.imwrite("abs_diff_new.png", diff_b)
#gray = cv2.cvtColor(diff_b,cv2.COLOR_BGR2GRAY)
#cv2.imshow('pair difference', gray)
#cv2.imwrite("gray_new.png" , gray)
#cv2.imwrite("hsv_diff_200.png",hsv)
#gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
#gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
#diff_g  = cv2.absdiff(gray1, gray2)
#cv2.imwrite("abs_diff_gray_rl.png", diff_g)
#cv2.imshow('diff_gray_200.png', diff_g)
#cv2.waitKey(5000)

#diff_o  = cv2.sub(diff_b, img1)
#cv2.imwrite("orig_diff.png", diff_o)
#diff_s = cv2.absdiff(diff_b, img2)
#cv2.imwrite("orig_diff_gray_rl.png", diff_s)
#mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

#th = 124
#imask =  mask>th

#canvas = np.zeros_like(img2, np.uint8)
#canvas[imask] = img2[imask]
#cv2.imshow('mask',canvas)
#cv2.waitKey(10000)
#cv2.imwrite("result.png", canvas)
