import os
os.environ["DISPLAY"] = ":0"


import time

import numpy as np
import cv2
from picamera2 import Picamera2, Preview,MappedArray

picam2 = Picamera2()

preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (800 , 600 )})
# preview_config = picam2.create_preview_configuration(main={"format": 'RGB888', "size": (800 , 600 )})
picam2.configure(preview_config)


cv2.startWindowThread()

picam2.start()


while True:
  img = picam2.capture_array()
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  #  (H, S, V)
  lower_val = np.array([50, 100, 170])
  upper_val = np.array([70, 255, 255])

  mask = cv2.inRange(hsv, lower_val, upper_val)

  # Find contours in the mask
  contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  for cont in contours:
  # if contours:
    # for every contour
      # Get the bounding box of the first contour
    x, y, w, h = cv2.boundingRect(cont)

    top_left = (x, y)
    bottom_right = (x + w, y + h)

    print("Top left coordinate:", top_left)
    print("Bottom right coordinate:", bottom_right)

      # Draw the bounding box on the original image (optional)
    cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)


  # else:
  #     print("No green mask found in the image.")

  # Display the image with bounding box (optional)
  cv2.imshow("Green Mask Bounding Box", img)
  cv2.waitKey(1)
    
