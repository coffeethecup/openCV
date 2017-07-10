# -*- coding: utf-8 -*-
# import the necessary packages
#http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
from collections import deque
import time
import datetime
import numpy as np
import argparse
import imutils
import cv2      #Video Library
import pymysql  #for mySQL DB connection
import requests #for POST request
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="goal",
                     db="goal")
cur = db.cursor()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#greenLower = (16, 86, 6)
greenLower = (22, 57, 168)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference to the webcam
#Logitech 1920x1080;1280*720;640x360
camera = cv2.VideoCapture(0)
camera.set(3,480) #Breite
camera.set(4,270) #Länge
#camera.set(5,1) #FPS

table_ID1=1
# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	#if args.get("video") and not grabbed:
		#break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = imutils.resize(frame, width=400)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		time_xy= datetime.datetime.now()
		print(x,y,time_xy)
                # ausgabe x,y Werte und speichern in der DB
                #print(x,y,time_xy)
		x2 = str(round(x,4))
		y2 = str(round(y,4))
		cur.execute("INSERT INTO xy(table_ID,x,y,timestamp) VALUES (%s,%s,%s,%s)",(table_ID1,x2,y2,time_xy))
		db.commit()
		#time.sleep(.05)
		#only proceed if the radius meets a minimum size
		if radius > 8:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# update the points queue
	pts.appendleft(center)
	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
