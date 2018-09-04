import argparse 
import json
import random
import cv2
import numpy as np
import sys

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, 
            np.float64)):
            return float(obj)
        elif isinstance(obj,(np.ndarray,)): #### This is the fix
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def randUniqueList(llist, n) :
  out = []
  while len(out) < n :
    t = random.choice(llist)
    try :
      out.index(t)
    except :
      out.append(t)
  return out

def addOneToList(llist, cur) :
  out = list(cur) # make a copy
  while True :
    t = random.choice(llist)
    try :
      out.index(t)
    except :
      out.append(t)
      return out

def fixProject(lp) :
  r = []
  for q in lp :
    r.append(q[0])
  r = np.array(r)
  return r


# attempt a calibration with a random set of calibration targets
def calibrationAttempt(pts, rows, cols) :
  global retL, mtxL, distL, rvecsL, tvecsL
  global retR, mtxR, distR, rvecsR, tvecsR
  objp = np.zeros((rows*cols, 3), np.float32)
  objp[:, :2] = np.mgrid[0:rows, 0:cols].T.reshape(-1, 2)

  objpoints = [] # 3D points in real world space
  imgpointsL = [] # 2D image points (left)
  imgpointsR = [] # 2D image points (right)
  ishape = None
  for p in pts :
    q = images[p]
    if ishape == None :
      ishape = q['leftshape']
    if not np.array_equal(ishape, q['leftshape']) :
      print 'left array of ' + str(p) + ' incorrect size '
      sys.exit(1)
    if not np.array_equal(ishape, q['rightshape']) :
      print 'right array of ' + str(p) + ' incorrect size '
      sys.exit(1)

    objpoints.append(objp)
    
    l = np.asfarray(q['leftpts'], dtype='float32')
    l = np.reshape(l, (-1, 2))
    imgpointsL.append(l)

    r = np.asfarray(q['leftpts'], dtype='float32')
    r = np.reshape(l, (-1, 2))
    imgpointsR.append(r)

  retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL, tuple(ishape[:-1]), None, None)
  retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR, tuple(ishape[:-1]), None, None)

  errL = 0
  for i in range(len(objpoints)) :
    lp, _ = cv2.projectPoints(objpoints[i], rvecsL[i], tvecsL[i], mtxL, distL)
    lp = fixProject(lp)
    t =  cv2.norm(imgpointsL[i], lp, cv2.NORM_L2) / len(lp)
    errL += t 
  errL = errL / len(objpoints)

  errR = 0
  for i in range(len(objpoints)) :
    rp, _ = cv2.projectPoints(objpoints[i], rvecsR[i], tvecsR[i], mtxR, distR)
    rp = fixProject(rp)
    t =  cv2.norm(imgpointsR[i], rp, cv2.NORM_L2) / len(rp)
    errR += t 
  errR = errR / len(objpoints)


  err = (errL + errR) / 2
  return err

def initializeSequence(images, args) :
  pts = randUniqueList(images.keys(), args.ssize)
  errMin = calibrationAttempt(pts, args.rows, args.cols)
  count = 0
  while True :
    print "Number of pairs " + str(len(pts)) + " error " + str(errMin)
    ptsp = addOneToList(images.keys(), pts)
    err = calibrationAttempt(ptsp, args.rows, args.cols)

    if err < errMin :
      errMin = err
      pts = ptsp
      count = 0
    else :
      count = count + 1
      if count >= args.ntries :
        break
      
  return (errMin, pts)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('json', help='json calibration target file')
  parser.add_argument('output', help='json calibration output file')
  parser.add_argument('--ssize', type=int, default=10, help='Image pair sample size')
  parser.add_argument('--rows', type=int, default=7, help='number of rows in calibration target')
  parser.add_argument('--cols', type=int, default=6, help='number of cols in calibration target')
  parser.add_argument('--onlyRaw', type=int, default=-1, help='If >0 then only do raw guesses and output value')
  parser.add_argument('--ntries', type=int, default=10, help='number of attempts to increase calibration set')
  parser.add_argument('--nprobes', type=int, default=10, help='number of probes into calibration space')
  args = parser.parse_args()

  with open(args.json, "r") as f :
    images = json.load(f)

  print args.onlyRaw
  if args.onlyRaw > 0 :
    print "Doing raw guesses (only) " + str(args.onlyRaw)
    for i in range(args.onlyRaw) :
      pts = randUniqueList(images.keys(), args.ssize)
      errMin = calibrationAttempt(pts, args.rows, args.cols)
      print str(i) + ", " + str(errMin) + ", " + str(len(pts))
  else :
    z = initializeSequence(images, args)
    best = z
    for i in range(args.nprobes) :
      z = initializeSequence(images, args)
      print z[0], len(z[1])
      if z[0] < best[0] :
        best = z
    print "Final calibration values "
    q = calibrationAttempt(z[1], args.rows, args.cols)
    print q
    calib={}
    calib['retL'] = retL
    calib['mtxL'] = mtxL
    calib['distL'] = distL
    calib['rvecsL'] = rvecsL
    calib['tvecsL'] = tvecsL
    calib['retR'] = retR
    calib['mtxR'] = mtxR
    calib['distR'] = distR
    calib['rvecsR'] = rvecsR
    calib['tvecsR'] = tvecsR
    calib['images'] = best[1]
    calib['err'] = best[0]


    dumped = json.dumps(calib, cls=NumpyEncoder)
    with open(args.output,"w") as outfile :
      json.dump(dumped, outfile)
