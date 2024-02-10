# forked from: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html

from __future__ import print_function
import cv2 as cv
import time
from picamera2 import Picamera2, Preview,MappedArray
import os
import serialapi
import sys
from staticvar import *
from queue import Queue 
from threading import Thread 
import json

def in_virtualenv():
    def get_base_prefix_compat():
        """Get base/real prefix, or sys.prefix if there is none."""
        return (
            getattr(sys, "base_prefix", None)
            or getattr(sys, "real_prefix", None)
            or sys.prefix
        )
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


default_config = {
    "low_H": 0,
    "high_H": max_value_H,
    "low_S": 0,
    "high_S": max_value,
    "low_V": 0,
    "high_V": max_value,
    "colorTolerance": 10,
    "h": 0,
    "s":0,
    "v":0,
    "baselineY": 517,
    "baselineRadius": 60,
    "baselineLeftX": 337,
    "baselineRightX":722
}

# load config from config.json
def loadConfig():
    with open('config.json') as f:
        data = json.load(f)
        return data

# Python code to merge dict using a single 
# expression
def Merge(dict1, dict2):
    res = dict1 | dict2
    return res


conf = Merge(default_config, loadConfig())
print("Starting with config:", conf)

def setConf(key, value):
    # print("UPDATING", key, value)
    global conf
    conf[key] = value

    with open('config.json', 'w') as f:
        json.dump(conf, f)

# baseline start
# x, y
# baselineLeft = (337, 517)
# baselineRight = (722, 517)
# baselineRadius = 60
# used for detecting the center dot for the robot arm

#! important: y should be the same, try to make this line parallel align with the pencil line on the robots base
# !TODO: use auto color detectiong for this in the future


# colorTolerance = 10 

#  used when recalcualting errorFromColor
# h, s, v = 0, 0, 0

def calcTolerance(H, S, V):
    setConf("h", H)
    setConf("s", S)
    setConf("v", V)
    global conf

    # tolerance 
    t = conf["colorTolerance"]
    setConf("low_H", int(max(0, min(255, H - t))))
    setConf("high_H", int(max(0, min(255, H + t))))
    setConf("low_S", int(max(0, min(255, S - t))))
    setConf("high_S", int(max(0, min(255, S + t))))
    setConf("low_V", int(max(0, min(255, V - t))))
    setConf("high_V", int(max(0, min(255, V + t))))


# ----------------- TRACKBARS ----------------
# name to confname mapping
trackBarConf = {
    "Low H": "low_H",
    high_H_name: "high_H",
    low_S_name: "low_S",
    high_S_name: "high_S",
    high_V_name: "high_V",
    low_V_name: "low_V",

}

def updateTrackbars():
    global conf
    for barName, confName in trackBarConf.items():
        cv.setTrackbarPos(barName, window_detection_name, conf[confName])


cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)

def updater(confName):
    def updateConf(val):
        setConf(confName, val)
        updateTrackbars()
        return 0
     
    return updateConf

# loop through the trackbars and run createTrackbar
for barName, confName in trackBarConf.items():
    # ! CLOUSER WARNING
    #! see: https://www.programiz.com/python-programming/closure#:~:text=When%20to%20use%20closures%3F
    cv.createTrackbar(barName, window_detection_name , conf[confName], max_value, updater(confName))

def on_colorTolerance_trackbar(val):
    setConf("colorTolerance", val)
    # set to current range
    calcTolerance(conf["h"], conf["s"], conf["v"])
    # update with correct values
    updateTrackbars()

# names are used to reference the trackbars, be careful when updating
cv.createTrackbar("Baseline Y", window_detection_name , conf["baselineY"], camHeight, lambda val: setConf("baselineY", val))
cv.createTrackbar("Baseline Left X", window_detection_name , conf["baselineLeftX"], camWidth, lambda val: setConf("baselineLeftX", val))
cv.createTrackbar("Baseline Right X", window_detection_name , conf["baselineRightX"], camWidth, lambda val: setConf("baselineRightX", val))
cv.createTrackbar("Color Tolerance", window_detection_name , conf["colorTolerance"], 70, on_colorTolerance_trackbar)
cv.createTrackbar("Baseline Radius", window_detection_name , conf["baselineRadius"], camWidth, lambda val: setConf("baselineRadius", val))

def click_event( event, x, y, flags, params): 
    img = frame

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
        calcTolerance(int(h), int(s), int(v))
        # update with correct values
        updateTrackbars()


def drawBox(mask, img):
    # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    tempImage = img
    for cont in contours:
        x, y, w, h = cv.boundingRect(cont)
        top_left = (x, y)
        bottom_right = (x + w, y + h)
        cv.rectangle(tempImage, top_left, bottom_right, (0, 255, 0), 2)

    return tempImage 

def drawBaseline(frame):
    global conf
    baselineLeft = (conf["baselineLeftX"], conf["baselineY"])
    baselineRight = (conf["baselineRightX"], conf["baselineY"])

    tempImg = cv.line(frame, baselineLeft, baselineRight, (0, 255, 0), 2)
    # calculate the center of the the baselines's x values
    center = (baselineLeft[0] + baselineRight[0]) // 2
    # draw a dot at the center of the baseline
    tempImg = cv.circle(tempImg, (center, baselineLeft[1]), 5, (0, 255, 0), -1)
    # draw a line from the baseline's center to the top of the screen
    tempImg = cv.line(tempImg, (center, baselineLeft[1]), (center, conf["baselineRadius"]), (0, 255, 0), 2)


    # !IMPORTANT: BASELINERADIUS STORES THE Y COORDINATE OF THE BASELINE 
    #  NOT THE SIZE OF THE RADIUS
    baseY = baselineLeft[1]
    radiusSize = (camHeight - conf["baselineRadius"]) - (camHeight - baseY)
    # draw coordinate system limits
    tempImg = cv.line(tempImg, (center -  radiusSize, baseY), (center +  radiusSize, baseY), (255, 255, 0), 2)
    return tempImg

lastTime = 0
def current_milli_time():
    return round(time.time() * 1000)


# this runs in an another thread
# to move arm:
# q.put((r, theta)) 
# radius: [distance from arm]
# theta: [angle from the center of the arm]
def serialThread(in_q, ser):
    
    while True: 
        # Get some data 
        data = in_q.get()

        r, theta = data
        # print("R", r)
        # print("Theta", theta)

        # move to theta
        serialapi.moveMotor(ser, 0, int(theta))
        serialapi.updateMotor(ser)
        time.sleep(0.001)

        # map radius (0 to 100)
        # to real units (14.5cm to 43.5cm)
        mappedRadius = map_range(r, 0, 100, 0, serialapi.radiusMax)
        # move to radius
        serialapi.armToCM(ser, mappedRadius, False)
        time.sleep(0.001)


    

q = Queue()
t1 = Thread(target = serialThread, args =(q, ser )) 
t1.start()



def moveArmTimer(mask, img):
    global lastTime
    # move arm every 500 ms
    throttle = 200
    doMove = False
    if (current_milli_time() - lastTime > throttle) :
        lastTime = current_milli_time()
        doMove = True
    
    return moveArm(mask, img,doMove )



def moveArm(mask, img, doMove): 
    global conf
    baselineLeft = (conf["baselineLeftX"], conf["baselineY"])
    baselineRight = (conf["baselineRightX"], conf["baselineY"])

    tempImage = img
    #TODO: optimize, this runs findContours twice
      # Find contours in the mask
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if not contours:
        # print("No contours found. Click to select a color to sample it. Adjust tolerance using slider. ")
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

    # !IMPORTANT
    # localX = map_range(x_avg, baselineLeft[0], baselineRight[0], -100, 100)
    # TODO: this only works if the baseline is parallel to the x axis
    # print("CHECK THIS THE PROBLEM IS HERE HOW IT MAPS")
    localY = map_range(y_avg, baselineLeft[1], conf["baselineRadius"], 0, 100)



    # !IMPORTANT: BASELINERADIUS STORES THE Y COORDINATE OF THE BASELINE 
    #  NOT THE SIZE OF THE RADIUS
    baseY = baselineLeft[1]
    radiusSize = (camHeight - conf["baselineRadius"]) - (camHeight - baseY)
    # draw coordinate system limits
    # tempImg = cv.line(tempImg, (center -  radiusSize, baseY), (center +  radiusSize, baseY), (255, 255, 0), 2)

    center = (baselineLeft[0] + baselineRight[0]) // 2


    localX = map_range(x_avg, (center -  radiusSize) , (center +  radiusSize), -100, 100)

    

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
    # print(int(final_theta))
    if (doMove):
        q.put((r, final_theta))

    return tempImage



while True:
    # capute this as an array
    # [y][x]
        # [0] b
        # [1] g
        # [2] r
    frame = picam2.capture_array()

    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #  this creates a mask
    frame_threshold = cv.inRange(frame_HSV, (conf["low_H"], conf["low_S"], conf['low_V']), (conf["high_H"], conf["high_S"], conf["high_V"]))
    
    cv.setMouseCallback(window_capture_name, click_event) 


    #  can be disabled
    withBox = frame
    # withBox = drawBox(frame_threshold, frame)

    trackBox = moveArmTimer(frame_threshold, withBox)

    withBase = drawBaseline(trackBox)

    
    cv.imshow(window_capture_name, withBase)
    cv.imshow(window_detection_name, frame_threshold)
    
    cv.waitKey(1)
