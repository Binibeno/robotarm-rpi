# importing the module 
import cv2 
from picamera2 import Picamera2
face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()
picam2 = Picamera2()
# not the max resolution
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (800 , 600 )}))
picam2.start()

clickposx = 50
clickposy = 50
r = 0 
g = 0
b = 0

title = "CLICK PIXEL FOR RGB/HSV"


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


# function to display the coordinates of 
# of the points clicked on the image  
def click_event(event, x, y, flags, params): 
    global clickposx
    global clickposy
    global title
    global r, g, b
    # checking for left mouse clicks 
    if event == cv2.EVENT_LBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        # print(x, ' ', y) 
        clickposx = x
        clickposy  = y

        # ! y,x
        b = img[y, x, 0] 
        g = img[y, x, 1] 
        r = img[y, x, 2] 
        print("RGB: ", r, g, b)
        # put it in the title variable
        title = "RGB: " + str(r) + " " + str(g) + " " + str(b)


        # HSV
        
        frame_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h = frame_HSV[y, x, 0] 
        s = frame_HSV[y, x, 1]
        v = frame_HSV[y, x, 2] 
        #! goes from 0-255
        
        h_standard, s_standard, v_standard = hsv_to_standard(h, s, v)
        h_standard = str(round(h_standard))
        s_standard = str(round(s_standard))
        v_standard = str(round(v_standard))
        #! standard, you can input this into google color picker and get about the same values if you were to input the RGB values
        print("HSV-standard: ", h_standard + "°,", s_standard + "%,",  v_standard + "%")
  
    # checking for right mouse clicks      
    if event==cv2.EVENT_RBUTTONDOWN: 
        clickposx = x
        clickposy  = y
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
  
        # displaying the coordinates 
        # on the image window 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        b = img[y, x, 0] 
        g = img[y, x, 1] 
        r = img[y, x, 2] 
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r), 
                    (x,y), font, 1, 
                    (255, 255, 0), 2) 
        cv2.imshow('image', img) 

   
  
while True:
    img = picam2.capture_array()
    # displaying the image 
    cv2.imshow('image', img) 


    # setting mouse handler for the image 
    # and calling the click_event() function 
    cv2.setMouseCallback('image', click_event) 

 
    cv2.setWindowTitle('image', title) 
    cv2.putText(img, str(clickposx) + ',' +
                   str(clickposy), (clickposx,clickposy), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 0, 0), 8) 
    # for outline
    cv2.putText(img, str(clickposx) + ',' +
                   str(clickposy), (clickposx,clickposy), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (int(b), int(g), int(r)), 2) 
    cv2.imshow('image', img) 
    
    # wait for a key to be pressed to exit 
    cv2.waitKey(1) 