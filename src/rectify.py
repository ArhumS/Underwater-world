import numpy as np
import cv2
import glob
import argparse

class StereoCalibration(object):
    def __init__(self, filepath):
        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.criteria_cal = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((7*6, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        self.objpoints = []  # 3d point in real world space
        self.imgpoints_l = []  # 2d points in image plane.
        self.imgpoints_r = []  # 2d points in image plane.

        self.cal_path = filepath
        self.read_images(self.cal_path)

    def read_images(self, cal_path):
        images_right = glob.glob(cal_path + '/right*.ppm')
        images_left = glob.glob(cal_path + '/left*.ppm')
        images_left.sort()
        images_right.sort()

        for i, fname in enumerate(images_right):
            print images_left[i]
            print images_right[i]
            self.img_l = cv2.imread(images_left[i])
            self.img_r = cv2.imread(images_right[i])

            self.img_l[:,:,0] = self.img_l[:,:,2]
            self.img_r[:,:,0] = self.img_r[:,:,2]

            self.gray_l = cv2.cvtColor(self.img_l, cv2.COLOR_BGR2GRAY)
            self.gray_r = cv2.cvtColor(self.img_r, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret_l, corners_l = cv2.findChessboardCorners(self.gray_l, (7, 6), None)
            ret_r, corners_r = cv2.findChessboardCorners(self.gray_r, (7, 6), None)

            # If found, add object points, image points (after refining them)
            self.objpoints.append(self.objp)
            print ret_l
            print ret_r

            if ret_l is True:
                rt = cv2.cornerSubPix(self.gray_l, corners_l, (11, 11),
                                      (-1, -1), self.criteria)
                self.imgpoints_l.append(corners_l)

                # Draw and display the left corners
                ret_l = cv2.drawChessboardCorners(self.img_l, (7, 6),
                                                  corners_l, ret_l)
                cv2.imshow(images_left[i], self.img_l)
                cv2.waitKey(1000)

            if ret_r is True:
                rt = cv2.cornerSubPix(self.gray_r, corners_r, (11, 11),
                                      (-1, -1), self.criteria)
                self.imgpoints_r.append(corners_r)

                # Draw and display the right corners
                ret_r = cv2.drawChessboardCorners(self.img_r, (7, 6),
                                                  corners_r, ret_r)
                cv2.imshow(images_right[i], self.img_r)
                cv2.waitKey(1000)
            self.img_shape = self.gray_l.shape[::-1]

        rt, self.M1, self.d1, self.r1, self.t1 = cv2.calibrateCamera(
            self.objpoints, self.imgpoints_l, self.img_shape, None, None)
        rt, self.M2, self.d2, self.r2, self.t2 = cv2.calibrateCamera(
            self.objpoints, self.imgpoints_r, self.img_shape, None, None)

        self.camera_model = self.stereo_calibrate(self.img_shape)

    def stereo_calibrate(self, dims):
        flags = 0
        flags |= cv2.CALIB_FIX_INTRINSIC
        # flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
        flags |= cv2.CALIB_USE_INTRINSIC_GUESS
        flags |= cv2.CALIB_FIX_FOCAL_LENGTH
        # flags |= cv2.CALIB_FIX_ASPECT_RATIO
        flags |= cv2.CALIB_ZERO_TANGENT_DIST
        # flags |= cv2.CALIB_RATIONAL_MODEL
        # flags |= cv2.CALIB_SAME_FOCAL_LENGTH
        # flags |= cv2.CALIB_FIX_K3
        # flags |= cv2.CALIB_FIX_K4
        # flags |= cv2.CALIB_FIX_K5
       
        stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER +
                                cv2.TERM_CRITERIA_EPS, 100, 1e-5)
        print "about to call"
        print 'Dimensions', dims
        print 'Dist co-eff camera 1', self.d1
        print 'Dist co-eff camera 2', self.d2
        print 'Camera matrix 1', self.M1
        print 'Camera matrix 2', self.M2
        print 'Rotatatioanal matrix r1',self.r1
        print 'Rotatatioanal matrix r2',self.r2
        print 'Translational matrix t1',self.t1
        print 'Translational matrix t2',self.t2
        print 'Dimension of dist-coeff 1', self.d1.shape
        print 'Dimension of dist-coeff 2', self.d2.shape
# for 2.4.8
        ret, M1, d1, M2, d2, R, T, E, F = cv2.stereoCalibrate(
            self.objpoints, self.imgpoints_l, self.imgpoints_r, dims, self.M1, 
            self.d1, self.M2, self.d2, criteria=stereocalib_criteria, flags=flags)
        self.gray_l = cv2.cvtColor(self.img_l, cv2.COLOR_BGR2GRAY)
        self.gray_r = cv2.cvtColor(self.img_r, cv2.COLOR_BGR2GRAY)
        
# outputs first camera matrix
        print('Intrinsic_mtx_1', M1)

# output vector of distortion coefficients 
        print('dist_1', d1)

# output second camera matrix
        print('Intrinsic_mtx_2', M2)

# output lens distortion coefficients for the second camera
        print('dist_2', d2)

# Output rotation & translational matrices between the 1st and the 2nd camera coordinate systems.
        print('R', R)
        print('T', T)

# E Output essential and Fundamental matrix.
        print('E', E)
        print('F', F)
        
        # for i in range(len(self.r1)):
        #     print("--- pose[", i+1, "] ---")
        #     self.ext1, _ = cv2.Rodrigues(self.r1[i])
        #     self.ext2, _ = cv2.Rodrigues(self.r2[i])
        #     print('Ext1', self.ext1)
        #     print('Ext2', self.ext2)
        camera_model = dict([('M1', M1), ('M2', M2), ('dist1', d1),('dist2', d2),
                             ('R',R), ('T',T),('E',E), ('F',F)])
        RL,RR,PL,PR,_, _,_ = cv2.stereoRectify(M1,M2,d1,d2 , self.gray_l.shape[::-1] ,R,T,alpha=-1)

        mapL1, mapL2 = cv2.initUndistortRectifyMap(M1, d1, RL, PL, self.gray_l.shape[::-1], cv2.CV_32FC1);
        mapR1, mapR2 = cv2.initUndistortRectifyMap(M1, d1, RR, PR, self.gray_r.shape[::-1], cv2.CV_32FC1);
        print 'RL', RL
        undistorted_rectifiedL = cv2.remap(self.img_l, mapL1, mapL2, cv2.INTER_LINEAR);
        undistorted_rectifiedR = cv2.remap(self.img_r, mapR1, mapR2, cv2.INTER_LINEAR);
        cv2.imshow(windowNameL,undistorted_rectifiedL);
        cv2.imshow(windowNameR,undistorted_rectifiedR);
        return camera_model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='String Filepath')
    args = parser.parse_args()
    cal_data = StereoCalibration(args.filepath)
    # print()
    # print("->>>> performing rectification")

    # keep_processing = True;
    # while (keep_processing):

# grab frames from camera (to ensure best time sync.)

           # camL.grab();
           # camR.grab();
 # then retrieve the images in slow(er) time (do not be tempted to use read() !)
  
           #   ret, frameL = camL.retrieve();
           #   ret, frameR = camR.retrieve();

# undistort & rectify based on the mapping,could improve interpolation and image border settings here

           
# start the event loop - essential

      #      key = cv2.waitKey(400) & 0xFF; # wait 40ms (i.e. 1000ms / 25 fps = 40 ms)


# It can also be set to detect specific key strokes by recording which key is pressed

 # e.g. if user presses "x" then exit

        #    if (key == ord('c')):
         #       keep_processing = False;
 
