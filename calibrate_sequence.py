import cv2
import numpy as np
import sys
import calib_points as cp
import validate_pairs as validate_pairs
import get_monocular as get_monocular

def calibrate_sequence(directory, display = False):
    """this fuction returns the calib points for every stereo pair in the directory """
    """ and saves calibration points file and calibrated image"""
    """this fuction also saves isvalid.npy file"""
 
  
    for pair in directory:
        frame = left[-8:]
        img_l = cv2.imread(l)
        img_r = cv2.imread(r)
        print (l)
        if display:           
             cv2.imshow('Image_left', img_l)
             cv2.waitKey(10)
             cv2.imshow('Image_Right',img_r)
             cv2.waitKey(10)
    
        imgpoint_l, objpoint_l, ret_c_l = cp.calib_points(img_l)
        imgpoint_r, objpoint_r, ret_c_r  = cp.calib_points(img_r)
 
        path = str(l)
        q = path.split('/')
        last = q[:-1]
        glue = '/'
        fix = glue.join(last)
        
        np.savetxt( fix + '/imgp_l.npz', np.asarray(imgpoint_l), delimiter=',')
        np.savetxt( fix + '/imgp_r.npz', np.asarray(imgpoint_r), delimiter=',')
        np.savetxt( fix + '/obj_pts.npz', objpoint_l, delimiter=',')
 
       
        if (len(imgpoint_l) == len(imgpoint_r)) and (len(imgpoint_l) == len(objpoint_r)):
           results = [1]
        else:
           results = [0]
        np.savetxt(fix + "/isvalid.npz" , results )

        if display :
            cv2.imshow('Drawn_L',ret_c_l)
            cv2.waitKey(10)
            cv2.imshow('Drawn_R',ret_c_r)
            cv2.waitKey(10)
                    
if __name__ == "__main__":
     if  len(sys.argv) == 2:
         print (sys.argv[1])
         calibrate_sequence(sys.argv[1],display = False)
     else:
        print('Usage : python3 calibrate_sequence.py  directory')
        



    
