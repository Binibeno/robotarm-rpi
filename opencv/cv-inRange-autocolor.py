# forked from: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html

from __future__ import print_function
import cv2 as cv
import argparse
import time
from picamera2 import Picamera2, Preview,MappedArray

import os
import serialapi


import sys

def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return (
        getattr(sys, "base_prefix", None)
        or getattr(sys, "real_prefix", None)
        or sys.prefix
    )

def in_virtualenv():
    return sys.prefix != get_base_prefix_compat()

if (not in_virtualenv()):
    print("Not in the virtual environment (virtualenv). See start.sh. Run source ~/mp/bin/activate from bash to active the virtual environment.")
    sys.exit()

# fix camera on ssh 
os.environ["DISPLAY"] = ":0"

picam2 = Picamera2()
# bgr
preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (800 , 600 )})
picam2.configure(preview_config)
picam2.start()

camHeight = 600
camWidth = 800

print("Starting serial communcation")
ser = serialapi.init_serial()

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection (mask)'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

colorTolerance =10 

#  used when recalcualting errorFromColor
h, s, v = 0, 0, 0
def errorFromColor(H, S, V):
    global h, s, v
    h = H
    s = S
    v = V

    # low_H should be: H - 10
    # high_H should be: H + 10

    global low_H, high_H, low_S, high_S, low_V, high_V, colorTolerance

    # tolerance 
    t = colorTolerance
    low_H = int(max(0, min(255, H - t)))
    high_H = int(max(0, min(255, H+t)))
    low_S = int(max(0, min(255, S-t)))
    high_S = int(max(0, min(255, S+t)))
    low_V = int(max(0, min(255, V-t)))
    high_V = int(max(0, min(255, V+t)))



def updateTrackbars():
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)
    cv.setTrackbarPos("Color Tolerance", window_detection_name, colorTolerance)


# forked from: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)




# baseline start
baselineLeft = (337, 517)
baselineRight = (722, 517)
baselineRadius = 60
# used for detecting the center dot for the robot arm

#! important: y should be the same, try to make this line parallel align with the pencil line on the robots base
# !TODO: use auto color detectiong for this in the future


def on_baselineLeft_trackbar(val):
    global baselineLeft
    baselineLeft = (val, baselineLeft[1])
    cv.setTrackbarPos("Baseline Left X", window_detection_name, val)

# baselineRight_trackbar
def on_baselineRight_trackbar(val):
    global baselineRight
    baselineRight = (val, baselineRight[1])
    cv.setTrackbarPos("Baseline Right X", window_detection_name, val)

# set y values for both baselines
def on_baselineY_trackbar(val):
    global baselineLeft
    global baselineRight
    baselineLeft = (baselineLeft[0], val)
    baselineRight = (baselineRight[0], val)
    cv.setTrackbarPos("Baseline Y", window_detection_name, val)
# baselineRadius_trackbar
def on_baselineRadius_trackbar(val):
    global baselineRadius
    baselineRadius = val
    cv.setTrackbarPos("Baseline Radius", window_detection_name, val)

def on_colorTolerance_trackbar(val):
    global colorTolerance 

    colorTolerance  = val
    cv.setTrackbarPos("Color Tolerance", window_detection_name, val)

    
    # set to current range
    errorFromColor(h, s, v)
    # update with correct values
    updateTrackbars()

cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)



# names are used to reference the trackbars, be careful when updating
cv.createTrackbar("Baseline Y", window_detection_name , baselineLeft[1], camHeight, on_baselineY_trackbar)
cv.createTrackbar("Baseline Left X", window_detection_name , baselineLeft[0], camWidth, on_baselineLeft_trackbar)
cv.createTrackbar("Baseline Right X", window_detection_name , baselineRight[0], camWidth, on_baselineRight_trackbar)
cv.createTrackbar("Baseline Radius", window_detection_name , baselineRadius, camWidth, on_baselineRadius_trackbar)

cv.createTrackbar("Color Tolerance", window_detection_name , 10, 70, on_colorTolerance_trackbar)


# like used in google color picker
def hsv_to_standard(h, s, v):
    # Ensure input values are within the valid range
    h = max(0, min(255, h))
    s = max(0, min(255, s))
    v = max(0, min(255, v))

    # Convert H, S, V to the standard range
    h_standard = (h / 255) * 360
    s_standard = (s / 255) * 100
    v_standard = (v / 255) * 100

    return h_standard, s_standard, v_standard



def click_event( event, x, y, flags, params): 
    img = cap

    # checking for left mouse clicks 
    if event == cv.EVENT_LBUTTONDOWN: 
  
        # ! y,x
        b = img[y, x, 0] 
        g = img[y, x, 1] 
        r = img[y, x, 2] 
        print("RGB: ", r, g, b)


        frame_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h = frame_HSV[y, x, 0] 
        s = frame_HSV[y, x, 1]
        v = frame_HSV[y, x, 2] 
        #! This is only used for processing inside opencv
        print("HSV-255max: ", h, s, v)
        
        h_standard, s_standard, v_standard = hsv_to_standard(h, s, v)
        # convert floats (h_standard, ...) to strings (with rounding!)
        h_standard = str(round(h_standard))
        s_standard = str(round(s_standard))
        v_standard = str(round(v_standard))
        #! standard, you can input this into google color picker and get about the same values if you were to input the RGB values
        print("HSV-standard: ", h_standard + "°,", s_standard + "%,",  v_standard + "%")
        # you can double check this using the google color picker!

        # set to current range
        errorFromColor(h, s, v)
        # update with correct values
        updateTrackbars()


def drawBox(mask, img):
      # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    tempImage = img
    for cont in contours:
    # if contours:
      # for every contour
        # Get the bounding box of the first contour
        x, y, w, h = cv.boundingRect(cont)

        top_left = (x, y)
        bottom_right = (x + w, y + h)

        #print("Top left coordinate:", top_left)
        #print("Bottom right coordinate:", bottom_right)

        # Draw the bounding box on the original image (optional)
        cv.rectangle(tempImage, top_left, bottom_right, (0, 255, 0), 2)

    return tempImage 




def drawBaseline(frame):
    tempImg = cv.line(frame, baselineLeft, baselineRight, (0, 255, 0), 2)
    # calculate the center of the the baselines's x values
    center = (baselineLeft[0] + baselineRight[0]) // 2
    # draw a dot at the center of the baseline
    tempImg = cv.circle(tempImg, (center, baselineLeft[1]), 5, (0, 255, 0), -1)
    # draw a line from the baseline's center to the top of the screen
    tempImg = cv.line(tempImg, (center, baselineLeft[1]), (center, baselineRadius), (0, 255, 0), 2)
    return tempImg

lastTime = 0
def current_milli_time():
    return round(time.time() * 1000)

def moveArmTimer(mask, img):
    global lastTime
    # move arm every 500 ms
    throttle = 200
    doMove = False
    if (current_milli_time() - lastTime > throttle) :
        lastTime = current_milli_time()
        doMove = True
    
    return moveArm(mask, img,doMove )



def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def moveArm(mask, img, doMove): 
    tempImage = img
    #TODO: optimize, this runs findContours twice
      # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("No contours found. Click to select a color to sample it. Adjust tolerance using slider. ")
        return tempImage
    
    top_left = [camWidth,camHeight]
    bottom_right = [0,0]
    
    for cont in contours:
     # Get the bounding box of the contour
        x, y, w, h = cv.boundingRect(cont)

        c_top_left = [x, y]
        c_bottom_right = [x + w, y + h]

        if c_top_left[0] < top_left[0]:
            top_left[0] = c_top_left[0]

        if c_top_left[1] < top_left[1]:
            top_left[1] = c_top_left[1]
        
        if c_bottom_right[0] > bottom_right[0]:
            bottom_right[0] = c_bottom_right[0]
        
        if c_bottom_right[1] > bottom_right[1]:
            bottom_right[1] = c_bottom_right[1]

    # ! top_left and bottom_right are now the coordinates of the detected object
    cv.rectangle(tempImage, top_left, bottom_right, (255, 0, 0), 2)
    
     
    # object coords
    x_avg = (top_left[0] + bottom_right[0]) // 2
    y_avg = (top_left[1] + bottom_right[1]) // 2

    #python cant divide by zero 
    x_avg = max(x_avg, 1)
    y_avg = max(y_avg, 1)



    #coordinate system
    #map baselineLeft and baselineRight to local coordinate system

    localX = map_range(x_avg, baselineLeft[0], baselineRight[0], -100, 100)
    # TODO: this only works if the baseline is parallel to the x axis
    # print("CHECK THIS THE PROBLEM IS HERE HOW IT MAPS")
    localY = map_range(y_avg, baselineLeft[1], baselineRadius, 0, 100)

    # print("Object in local coordinate system", localX, localY)
    # (-100 to 100)
    
    # theta is the angle 
    (r, theta_original) =serialapi.descartesToPolar(localX, localY)

    
    # positive range (from 0 to 180)
    new_theta = theta_original + 90

    final_theta = new_theta

    if new_theta >= 360:
        final_theta = new_theta - 360

    elif (new_theta < 0):
        final_theta = new_theta + 360

    else:
        final_theta = new_theta
    
    radius = r
    print(int(final_theta))
    if (doMove):
        serialapi.moveMotor(ser, 0, int(final_theta))
        serialapi.updateMotor(ser)
        time.sleep(0.001)
    return tempImage


# config save loader
# multithread
while True:
    cap = picam2.capture_array()
    frame = cap

    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #  this creates a mask
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    
    cv.setMouseCallback(window_capture_name, click_event) 


    #  can be disabled
    withBox = frame
    # withBox = drawBox(frame_threshold, frame)

    trackBox = moveArmTimer(frame_threshold, withBox)

    withBase = drawBaseline(trackBox)


    
    cv.imshow(window_capture_name, withBase)
    cv.imshow(window_detection_name, frame_threshold)
    
    cv.waitKey(1)
