# threshold_HSV.py
# This program uses thresholding to track a ball.
# It demonstrates the use of HSV thresholding to detect an object

import cv2
import numpy as np
import os
import tkinter as Tk
# Define some global variables
# initial min and max HSV filter values.
# these will be changed using trackbars
# Some boolean variables for different functionality within this  program
DEBUG = 0
H_MIN = 0
H_MAX = 180 
S_MIN = 0
S_MAX = 256
V_MIN = 0
V_MAX = 256
H_TEXT = "H_MIN = " + str(H_MIN) + " H_MAX = " + str(H_MAX) + "\n" 
S_TEXT = "S_MIN = " + str(S_MIN) + " S_MAX = " + str(S_MAX) + "\n"
V_TEXT = "V_MIN = " + str(V_MIN) + " V_MAX = " + str(V_MAX) + "\n"
#EAP LEFT OFF HERE TRYING TO GET TK WINDOW TO UPDATE
root = Tk.Tk()
root.title("Slider Values")
ALL_TEXT = Tk.StringVar()
ALL_TEXT.set(H_TEXT + S_TEXT + V_TEXT)
label = Tk.Label(root, textvariable=ALL_TEXT).pack()
# default capture width and height
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
# max number of objects to be detected in frame
MAX_NUM_OBJECTS=50
# minimum and maximum object area
MIN_OBJECT_AREA = 20*20
MAX_OBJECT_AREA = FRAME_HEIGHT*FRAME_WIDTH/1.5
# names that will appear at the top of each window
windowName = "Original Image"
windowName1 = "HSV Image"
windowName2 = "Thresholded Image"
windowName3 = "After Morphological Operations"
trackbarWindowName = "Trackbars"


def on_trackbar(message):
# This function gets called whenever a
# trackbar position is changed
    global H_MIN 
    global H_MAX 
    global S_MIN 
    global S_MAX 
    global V_MIN 
    global V_MAX 
    global ALL_TEXT
    H_MIN_NEW = cv2.getTrackbarPos("H_MIN", trackbarWindowName)
    H_MAX_NEW = cv2.getTrackbarPos("H_MAX", trackbarWindowName)
    S_MIN_NEW = cv2.getTrackbarPos("S_MIN", trackbarWindowName)
    S_MAX_NEW = cv2.getTrackbarPos("S_MAX", trackbarWindowName)
    V_MIN_NEW = cv2.getTrackbarPos("V_MIN", trackbarWindowName)
    V_MAX_NEW = cv2.getTrackbarPos("V_MAX", trackbarWindowName)
    if(DEBUG):
     if(H_MIN_NEW != H_MIN and DEBUG == 1 ):
      print ( "H_MIN was " + str(H_MIN) + " H_MIN no set to " + str(H_MIN_NEW) +"\n")
    if(DEBUG):
     if(H_MAX_NEW != H_MAX and DEBUG == 1 ):
      print ( "H_MAX was " + str(H_MAX) + " H_MAX no set to " + str(H_MAX_NEW) +"\n")
     if(S_MIN_NEW != S_MIN and DEBUG == 1 ):
      print ( "S_MIN was " + str(S_MIN) + " S_MIN no set to " + str(S_MIN_NEW) +"\n")
    if(DEBUG):
     if(S_MAX_NEW != S_MAX and DEBUG == 1 ):
      print ( "S_MAX was " + str(S_MAX) + " S_MAX no set to " + str(S_MAX_NEW) +"\n")
     if(V_MIN_NEW != V_MIN and DEBUG == 1 ):
      print ( "V_MIN was " + str(V_MIN) + " V_MIN no set to " + str(V_MIN_NEW) +"\n")
    if(DEBUG):
     if(V_MAX_NEW != V_MAX and DEBUG == 1 ):
      print ( "V_MAX was " + str(V_MAX) + " V_MAX no set to " + str(V_MAX_NEW) +"\n")
    H_MIN = H_MIN_NEW
    H_MIN = H_MIN_NEW
    H_MAX = H_MAX_NEW
    S_MIN = S_MIN_NEW
    S_MAX = S_MAX_NEW
    V_MIN = V_MIN_NEW
    V_MAX = V_MAX_NEW
    H_TEXT = "H_MIN = " + str(H_MIN) + " H_MAX = " + str(H_MAX) + "\n"
    S_TEXT = "S_MIN = " + str(S_MIN) + " S_MAX = " + str(S_MAX) + "\n"
    V_TEXT = "V_MIN = " + str(V_MIN) + " V_MAX = " + str(V_MAX) + "\n"
    ALL_TEXT.set(H_TEXT + S_TEXT + V_TEXT) 

def createTrackbars(name):
# create window for trackbars

    cv2.namedWindow(name,0)
# create trackbars and insert them into window
# 3 parameters are: the address of the variable that is changing when the trackbar is moved(eg.H_LOW),
# the max value the trackbar can move (eg. H_HIGH), 
# and the function that is called whenever the trackbar is moved(eg. on_trackbar)
#                                   ---->    ---->     ---->      
    cv2.createTrackbar( "H_MIN", name, H_MIN, H_MAX, on_trackbar )
    cv2.createTrackbar( "H_MAX", name, H_MAX, H_MAX, on_trackbar )
    cv2.createTrackbar( "S_MIN", name, S_MIN, S_MAX, on_trackbar )
    cv2.createTrackbar( "S_MAX", name, S_MAX, S_MAX, on_trackbar )
    cv2.createTrackbar( "V_MIN", name, V_MIN, V_MAX, on_trackbar )
    cv2.createTrackbar( "V_MAX", name, V_MAX, V_MAX, on_trackbar )



#######################################################
# All code below here is main                         #
#######################################################
#on_trackbar(MAX_NUM_OBJECTS)
capWebcam = cv2.VideoCapture(0) # declare a VideoCapture object and associate to webcam, 0 => use 1st webcam
print ( "default resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
capWebcam.set(cv2.CAP_PROP_FRAME_WIDTH, 320.0)              # change resolution to 320x240 for faster processing
capWebcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240.0)
print ( "updated resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
if capWebcam.isOpened() == False:                           # check if VideoCapture object was associated to webcam successfully
   print ( "error: capWebcam not accessed successfully\n\n")         # if not, print error message to std out
   os.system("pause")                                              # pause until user presses a key so user can see error message
createTrackbars(trackbarWindowName)
while cv2.waitKey(1) != 27 and capWebcam.isOpened():  # until the Esc key is pressed or webcam connection is lost
      blnFrameReadSuccessfully, imgOriginal = capWebcam.read()            # read next frame
      if not blnFrameReadSuccessfully or imgOriginal is None:             # if frame was not read successfully
            print ( "error: frame not read from webcam\n")                    # print error message to std out
            os.system("pause")                                              # pause until user presses a key so user can see error message
            break                                                           # exit while loop (which exits program)
      imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
      imgThresh = cv2.inRange(imgHSV, np.array([H_MIN, S_MIN, V_MIN]), np.array([H_MAX, S_MAX, V_MAX]))
      intRows, intColumns = imgThresh.shape
      circles = cv2.HoughCircles(imgThresh, cv2.HOUGH_GRADIENT, 5, intRows / 4)      # fill variable circles with all circles in the processed image
      if circles is not None:  # this line is necessary to keep program from crashing on next line if no circles were found
         for circle in circles[0]:                           # for each circle
          x, y, radius = circle                                                                       # break out x, y, and radius
          print ( "ball position x = " + str(x) + ", y = " + str(y) + ", radius = " + str(radius))       # print ball position and radius 
          cv2.circle(imgOriginal, (x, y), 3, (0, 255, 0), -1)           # draw small green circle at center of detected object
          cv2.circle(imgOriginal, (x, y), radius, (0, 0, 255), 3)                     # draw red circle around the detected object

      cv2.imshow(windowName2,imgThresh);
      cv2.imshow(windowName,imgOriginal);
