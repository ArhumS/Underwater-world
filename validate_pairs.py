import sys
from get_monocular import get_monocular
import numpy as np

def validate_pairs(directory, width = 4):
    
    """ this function validates the directory structure """
    left = get_monocular(directory, 'frame_*/left.jpg')
    right = get_monocular(directory, 'frame_*/right.jpg')

    if len(left) != len(right):
        print(f"left length {len(left)} right length {len(right)}")
        return False
    
    for counter, l, r in zip(range(1,len(left)+1),left,right):
 #       print(f" counter {counter} left {l} right {r}")
        numstring = format(counter, '0'+ str(width))
          
        left_name = f"{directory}/frame_{numstring}/left.jpg"
        right_name = f"{directory}/frame_{numstring}/right.jpg"
       
        if left_name != l:
            print(f"left {left_name} != {l}")
            return False
        if right_name != r:
            print(f"right {right_name} != {r}")
            return False 
    return True

if __name__ == "__main__":

    if  len(sys.argv) == 2:
        print(validate_pairs(sys.argv[1]))
    else:
        print('Usage : python3 validate_pairs.py directory')
        
