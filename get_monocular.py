import glob
import sys

def get_monocular(directory, pattern):
    """ return list of monocular frames """ 

    imgs = glob.glob(directory  + '/'  + pattern)
    return (imgs)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(get_monocular(sys.argv[1], sys.argv[2]))
    else:
        print('Usage : python3 get_monocular.py directory pattern')
 
