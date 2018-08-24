#!/usr/bin/env python
#
# Extract frames from a stereo video file
#
import sys
import os

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "usage: extractFrames.py video vid-dir"
  else:
    if os.path.exists(sys.argv[2]):
      print "Output directory " + sys.argv[2] + " already exists"
      sys.exit(1)
    os.mkdir(sys.argv[2])
    os.system("./ffmpeg -i " + sys.argv[1] + " -map 0:0 -vcodec copy -an " + sys.argv[2] + "/left.avi")
    os.system("./ffmpeg -i " + sys.argv[1] + " -map 0:2 -vcodec copy -an " + sys.argv[2] + "/right.avi")
    os.system("./ffmpeg -i " + sys.argv[2] + "/left.avi -an " + sys.argv[2] + "/left.%010d.ppm")
    os.system("./ffmpeg -i " + sys.argv[2] + "/right.avi -an " + sys.argv[2] + "/right.%010d.ppm")
