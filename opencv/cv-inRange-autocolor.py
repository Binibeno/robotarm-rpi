# forked from: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html

from __future__ import print_function
import cv2 as cv
import argparse

from picamera2 import Picamera2, Preview,MappedArray

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (800 , 600 )})
picam2.configure(preview_config)
picam2.start()



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

def errorFromColor(H, S, V):
    # low_H should be: H - 10
    # high_H should be: H + 10

    global low_H, high_H, low_S, high_S, low_V, high_V

    
    low_H = int(max(0, min(255, H - 10)))
    high_H = int(max(0, min(255, H+10)))
    low_S = int(max(0, min(255, S-10)))
    high_S = int(max(0, min(255, S+10)))
    low_V = int(max(0, min(255, V-10)))
    high_V = int(max(0, min(255, V+10)))


    
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




cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)


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




while True:
    cap = picam2.capture_array()
    frame = cap

    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    
    cv.setMouseCallback(window_capture_name, click_event) 
    
    cv.imshow(window_capture_name, frame)
    cv.imshow(window_detection_name, frame_threshold)
    
    cv.waitKey(1)
