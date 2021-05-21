import numpy as np
import random
import sys
import valid_npy as vf

def create_seed(valid_frames, seed = 10):
  '''This function returns 10 seeded frames & random frames from valid frame list'''

  seed_frames = random.sample(valid_frames,seed)
    
  resid = []
  for s in valid_frames:
    if not(s in seed_frames):
        resid.append(s)
  return seed_frames,resid

if __name__ == "__main__":
    if  len(sys.argv) == 2:
        valid_frames = vf.valid_npy(sys.argv[1], width = 4)
        print ("seeds are...." , create_seed(valid_frames))
    else:
        print('Usage : python3 create_seed.py  directory')

