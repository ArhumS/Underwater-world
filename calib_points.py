import cv2
import numpy as np

def calib_points(img, grid = (7,9), criteria1 = 30, criteria2 = 0.001):
    """ return calibration points from calibration target """
 
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, criteria1, criteria2)
    objp = np.zeros((grid[0]*grid[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:grid[1],0:grid[0]].T.reshape(-1,2)
    objp = objp.reshape(-1,1,3)
    axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
    ret, corners = cv2.findChessboardCorners(gray, grid , None)
    ret_c = cv2.drawChessboardCorners(img, grid, corners, ret)
    objpoints = []
    imgpoints = []
 
    if ret:
         
         corners = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
         
 #        corners.shape = (corners.shape[0],corners.shape[2])

 #        objp.shape = (objp.shape[0],objp.shape[2])
         objpoints.append(objp)
         imgpoints.append(corners)
         ret_cl, mtx_l, dist_l, rvec_l, tvec_l = cv2.calibrateCamera(objpoints,imgpoints, gray.shape[::-1], None, None)
         print (objpoints)
         print(imgpoints)
 
 
         return corners, objp, ret_c
    else:
         print('None')
         return None, None

if __name__ == "__main__":
        
    img = cv2.imread('left.1.jpg')
    cv2.imshow('xxx', img)
    cv2.waitKey(0)

    imgpoint, objpoint, ret_c = calib_points(img)
 #   print('obj point',objpoint)
    cv2.imshow('yyy', ret_c)
    cv2.waitKey(0)
 
    

