import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont

font = cv2.FONT_HERSHEY_PLAIN

img = cv2.imread('Difference_200.png')
test1 =cv2.imread('left.200.ppm')
test2 =cv2.imread('left.201.ppm')
col_map = cv2.imread('colour_diff_200.png')
o_quiver = cv2.imread('Op1.png')
orig_diff = cv2.imread('orig_diff_200.png')
orig_diff_2 = cv2.imread('colour_diff_d_200.png')
gray = cv2.imread('gray_200.png')
i= ('b','g')
#for i,col in enumerate(color):
histr = cv2.calcHist([test1],[i], None,[256],[0,255])
plt.subplot(241), plt.imshow(test1) ,plt.title('Original-001'),
plt.xlabel('(a)', fontsize=18)
plt.subplot(242), plt.imshow(test2) ,plt.title('Original-002'),
plt.xlabel('(a)', fontsize=18)
#cv2.putText(test,'Brightest region',(600,600), font, 2,(0,0,0),2,False)
plt.subplot(243), plt.imshow(gray,'gray'), plt.title('Image Difference')
plt.xlabel('(b)', fontsize=18)
#cv2.putText(img,'Fastest motion region',(450,690), font, 2,(200,0,0),2,False)

plt.subplot(244), plt.imshow(img,'gray'),plt.title('Image Difference_rgb'),
plt.xlabel('(c)', fontsize=18)
plt.subplot(245), plt.imshow(col_map,'gray'),plt.title('Heat map'),
plt.subplot(246), plt.imshow(orig_diff,'gray'),plt.title('Reduced caustic'),
plt.subplot(248), plt.hist(gray.ravel(),256,[0,256],color=['magenta'])
plt.plot(histr)
plt.title('Histogram of test 1')
plt.xlabel('(d)', fontsize=18)
plt.xlim([0,255])
plt.subplot(247), plt.imshow(orig_diff_2,'gray'),plt.title('Heat map Gray'),
plt.savefig('Histogram.png')

plt.show()

