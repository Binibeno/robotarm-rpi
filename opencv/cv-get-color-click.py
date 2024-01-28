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

title = "CLICK TO GRAB RGB"

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
        print(x, ' ', y) 
        clickposx = x
        clickposy  = y


        
        # ! y,x
        b = img[y, x, 0] 
        g = img[y, x, 1] 
        r = img[y, x, 2] 
        print("RGB: ", r, g, b)
        # put it in the title variable
        title = "RGB: " + str(r) + " " + str(g) + " " + str(b)


        # displaying the coordinates 
        # on the image window 
        # font = cv2.FONT_HERSHEY_SIMPLEX 
        # cv2.putText(img, str(x) + ',' +
        #             str(y), (x,y), font, 
        #             1, (255,0,0), 2) 
        # cv2.imshow('image', img) 


  
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