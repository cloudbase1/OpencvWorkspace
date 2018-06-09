# ball_tracker_mac.py

# to run this program, type:
# sudo python ball_tracker_mac.py headed          (GUI)
# sudo python ball_tracker_mac.py headless        (no GUI (for embedded use))

# this program is used to send position information of the ball on the PID balance demo

# use the circuit from "pan_and_tilt_tracker.png"

import cv2
import numpy as np
import os
import sys
import platform
from operator import itemgetter

###################################################################################################
def main():
    headed_or_headless = ""

    if len(sys.argv) == 2 and str(sys.argv[1]) == "headed":
        headed_or_headless = "headed"
        print ("entering headed mode")
    elif len(sys.argv) == 2 and str(sys.argv[1]) == "headless":
        headed_or_headless = "headless"
        print ("entering headless mode")
    else:
        print ("\nprogram usage:\n")
        print ("for headed mode (GUI interface) @command prompt type: sudo python ball_tracker.py headed\n")
        print ("for headless mode (no GUI interface, i.e. embedded mode) @ command prompt type: sudo python ball_tracker.py headless\n")
        return
    # end if else

    #capWebcam = cv2.VideoCapture(1)  # declare a VideoCapture object and associate to webcam, 0 => use 1st webcam
    capWebcam = cv2.VideoCapture(0)  # declare a VideoCapture object and associate to webcam, 0 => use 1st webcam
    print("OpenCV Version: {}".format(cv2.__version__))
    print("Python Version: {}".format(platform.python_version()))
    print ("default resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    capWebcam.set(cv2.CAP_PROP_FRAME_WIDTH, 320.0)
    capWebcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240.0)

    print ("updated resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    if capWebcam.isOpened() == False:                           # check if VideoCapture object was associated to webcam successfully
        print ("error: capWebcam not accessed successfully\n\n")          # if not, print error message to std out)
        os.system("pause") # pause until user presses 
        return            
    # end if

    intXFrameCenter = int(float(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) / 2.0)
    intYFrameCenter = int(float(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) / 2.0)

    while cv2.waitKey(1) != 27 and capWebcam.isOpened():                # until the Esc key is pressed or webcam connection is lost
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()            # read next frame

        if not blnFrameReadSuccessfully or imgOriginal is None:             # if frame was not read successfully
            print ("error: frame not read from webcam\n")                     # print error message to std out)
            os.system("pause")                                              # pause until user presses a key so user can see error message
            break                                                           # exit while loop (which exits program)
        # end if
        imgBlur = cv2.medianBlur(imgOriginal,11)
        # Add HSV color filter before grey
        imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
        # Filter HSV image
        mask = cv2.inRange(imgHSV, np.array([26, 61, 30]), np.array([40, 256, 256]))
        # Bitwise-AND mask and original image
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        imgRes = cv2.bitwise_and(imgGray,mask)

        circles = cv2.HoughCircles(imgRes, cv2.HOUGH_GRADIENT,3,100, param1=1,param2=50,minRadius=1,maxRadius=50) 
        #circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, 5, 20)      # fill variable circles with all circles in the processed image

        if circles is not None:                     # this line is necessary to keep program from crashing on next line if no circles were found
         for circle in circles[0]:                           # for each circle
           x, y, radius = circle  
           print ("ball position x = " + str(x) + ", y = " + str(y) + ", radius = " + str(radius))       # print ball position and radius

         # end if else

           if headed_or_headless == "headed":
                cv2.circle(imgOriginal, (x, y), 3, (0, 255, 0), 1)           # draw small green circle at center of detected object
                cv2.circle(imgOriginal, (x, y), radius, (0, 0, 255), 3)       # draw red circle around the detected object
            # end if

        # end if

        if headed_or_headless == "headed":
                            # show windows
            cv2.imshow("imgGray", imgGray)
            cv2.imshow("imgHSV", imgHSV)
            cv2.imshow("mask", mask)
            cv2.imshow("imgBlur", imgBlur)
            cv2.imshow("imgRes", imgRes)
            cv2.imshow("imgOriginal", imgOriginal) 
        # end if
    # end while

    cv2.destroyAllWindows()                     # remove windows from memory

    return
# end main

###################################################################################################

###################################################################################################
if __name__ == "__main__":
    main()
















