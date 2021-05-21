import cv2
import numpy as np
import calib_points as cp
import valid_npy as npy
import create_seed as cs
import sys    

def calib_from_list(frame_list , directory , frame_dims = (1280,720), width = 4 , h = 1380, w = 720):
  objpoints = []
  imgpoints_l = []
  imgpoints_r = []
  
  for i in frame_list:
         numstring = format(i, '0' + str(width))
         p1 = f"{directory}/frame_{numstring}/imgp_l.npz"
         p2 = f"{directory}/frame_{numstring}/imgp_r.npz"
         p3 = f"{directory}/frame_{numstring}/obj_pts.npz"

         imgp_l = np.loadtxt(p1, delimiter = ',')
         imgp_r = np.loadtxt(p2, delimiter = ',')
         obj_p = np.loadtxt(p3, delimiter = ',')

         obj_p = obj_p.astype(np.float32)
         obj_p = obj_p.reshape(-1,1,3)
 
         imgp_l = imgp_l.astype(np.float32)
         imgp_r = imgp_r.astype(np.float32)
         imgp_l = imgp_l.reshape(-1,1,2)
         imgp_r = imgp_r.reshape(-1,1,2)
        
         imgpoints_l.append(imgp_l)
         imgpoints_r.append(imgp_r)
         objpoints.append(obj_p)
         
 
  ret_cl, mtx_l, dist_l, rvec_l, tvec_l = cv2.calibrateCamera(objpoints,imgpoints_l, frame_dims, None, None)
  ret_cr, mtx_r, dist_r, rvec_r, tvec_r = cv2.calibrateCamera(objpoints,imgpoints_r, frame_dims, None, None)
      
  flags = 0
  flags = cv2.CALIB_ZERO_DISPARITY
  
  stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 100, 1e-5)
  ret, mtx_l, dist_l, mtx_r, dist_r, R, T, E, F = cv2.stereoCalibrate(objpoints,imgpoints_l, imgpoints_r, mtx_l, dist_l, mtx_r, dist_r, frame_dims, flags=flags, criteria=stereocalib_criteria)

  return  ret, mtx_l, dist_l, mtx_r, dist_r, R, T, E, F


if __name__ == "__main__":
    if  len(sys.argv) == 2:
        valid_frames = npy.valid_npy(sys.argv[1], width = 4)
        frames,seed = cs.create_seed(valid_frames)
        print (calib_from_list(frames,directory = sys.argv[1]))
    else:
        print('Usage : python3 calib_from_list.py  directory')       
