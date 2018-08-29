# Computing Reprojection error (residual-1)
# camera 1
tot_error_c1=0
total_points_c1=0
for k1 in xrange(len(objpoints)):
    reprojected_points_c1, _ = cv2.projectPoints(objpoints[k1], rvecs1[k1], tvecs1[k1], M1, d1)
    reprojected_points_c1 =reprojected_points.reshape(-1,2)
    tot_error_c1 += np.sum(np.abs(imgpoints[k1]-reprojected_points_c1)**2)
    total_points_c1 +=len(objpoints[k1])
mean_error_c1 =np.sqrt(tot_error_c1 /total_points_c1)
print "Camera 1_reprojection error: ", mean_error_c1

#camera 2
tot_error_c2=0
total_points_c2=0
for k2 in xrange(len(objpoints)):
    reprojected_points_c2, _ = cv2.projectPoints(objpoints[k2], rvecs2[k2], tvecs2[k2], M2, d2)
    reprojected_points_c2 =reprojected_points.reshape(-1,2)
    tot_error_c2 += np.sum(np.abs(imgpoints[k2]-reprojected_points_c2)**2)
    total_points_c2 += len(objpoints[k2])
mean_error_c2 =np.sqrt(tot_error_c2 /total_points_c2)
print "Camera 2_reprojection error: ", mean_error_c2

# Computing Mean error
mean_rep = (mean_error_c1 + mean_error_c2) / 2
print "Mean stereo error ", mean_rep

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='String Filepath')
    args = parser.parse_args()
    cal_data = StereoCalibration(args.filepath)


