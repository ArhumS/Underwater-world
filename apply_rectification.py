import calib_from_list as calib_st
import cv2
import sys
import valid_npy as npy
import numpy as np
import create_seed as cs

def apply_rectification(frame_list, directory, frame_dims = (1280,720) , width = 4):

  for i in frame_list:
        numstring = format(i, '0' + str(width))
        p1 = f"{directory}/frame_{numstring}/left.jpg"
        p2 = f"{directory}/frame_{numstring}/right.jpg"
         
        img_l = cv2.imread(p1)
        img_r = cv2.imread(p2)
        h,w = img_l.shape[:2]
        
        ret, mtx_l, dist_l, mtx_r, dist_r, R, T, E, F  = calib_st.calib_from_list(frames,directory)

        R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(mtx_l, dist_l, mtx_r, dist_r, frame_dims, R,T)

        w1,h1 = 5*w,5*h

        newCam_l, roi = cv2.getOptimalNewCameraMatrix(mtx_l,dist_l,frame_dims,1,(w1,h1))
        newCam_r, roi = cv2.getOptimalNewCameraMatrix(mtx_r,dist_r,frame_dims,1,(w1,h1))
 
        lmaps = cv2.initUndistortRectifyMap(mtx_l, dist_l, None, newCam_l, (w1,h1), 5)
        rmaps = cv2.initUndistortRectifyMap(mtx_r, dist_r, None, newCam_r, (w1,h1), 5)
    
        dst_l = cv2.remap(img_l, lmaps[0], lmaps[1], cv2.INTER_LINEAR)        
        dst_r = cv2.remap(img_r, rmaps[0], rmaps[1], cv2.INTER_LINEAR)

        dst_l = cv2.resize(dst_l ,None, fx=.5, fy=.5, interpolation = cv2.INTER_CUBIC)
        dst_r = cv2.resize(dst_r ,None, fx=.5, fy=.5, interpolation = cv2.INTER_CUBIC)
        
        numpy_h = np.hstack((dst_l, dst_r))
        cv2.imshow("rectified" , numpy_h)
        cv2.waitKey(500)

#        with open('lmaps.txt', 'wb') as f:
 #           np.savetxt(f, lmaps[0])
#            np.savetxt(f, lmaps[1])
        
 #       cv2.imwrite(directory + '/frame_'   + str(i).zfill(4) + '/l_rect.jpg' , rect_L)
 #       cv2.imwrite(directory + '/frame_'   + str(i).zfill(4) + '/r_rect.jpg' , rect_R)

  return  R1, R2, P1, P2, Q, dst_r

if __name__ == "__main__":
    if  len(sys.argv) == 2:
        valid_frames = npy.valid_npy(sys.argv[1], width = 4)
        frames,seed = cs.create_seed(valid_frames)
        R1, R2, P1, P2, Q, dst_r= apply_rectification(frames,directory = sys.argv[1])
    else:
        print('Usage : python3 apply_rectification.py  directory')       


