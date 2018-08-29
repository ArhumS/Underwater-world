import json
import random
import cv2
import numpy as np

def randUniqueList(list, n) :
  out = []
  while len(out) < n :
    t = random.choice(list)
    try :
      out.index(t)
    except :
      out.append(t)
  return out

#load json- text file (same directory)
with open("info.txt", "r") as f :
  images = json.load(f)

# choose 10 random images
pts = randUniqueList(images.keys(), 10)
for p in pts :
  q = images[p]
  l = np.asarray(q['leftpts'])
  r = np.asarray(q['rightpts'])
  print 'printing out frame ' + str(q['left']) + ' ' + str(q['right'])
  leftfile = q['left']
  shape = cv2.imread(leftfile).shape
  
print l
print 'done'
print 'shape is ' + str(shape)
print shape[0:2]



