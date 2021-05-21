import os.path
import numpy as np
import sys
import get_monocular as get_monocular

def valid_npy(directory, width = 4):

    ''' This function returns a list of all valid and invalid frames'''
    vfile = get_monocular.get_monocular(directory, 'frame_*')
    l = len(vfile)
    
    valid_list = []
 
    for i in range(1,l+1):
         numstring = format(i, '0' + str(width))
         p = f"{directory}/frame_{numstring}/isvalid.npz"
         
         if os.path.exists(p):
 #           print('Path exists')
          
            x = np.loadtxt(directory + '/frame_' + str(i).zfill(width) + '/isvalid.npz')
            if x == [1.0] :
 #                print ('Pair_is_valid')
                 valid_list.append(i)
    
    return (valid_list)

if __name__ == "__main__":
    if  len(sys.argv) == 2:
         print ("valid frames are ...  " , valid_npy(sys.argv[1]))
    else:
        print('Usage : python3 valid_npy.py  directory')
