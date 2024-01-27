import os
os.environ["DISPLAY"] = ":0"


import time

import numpy as np
import cv2
from picamera2 import Picamera2, Preview,MappedArray

picam2 = Picamera2()

cv2.startWindowThread()


preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (800 , 600 )})
picam2.configure(preview_config)
# callback - here I can use opencv
# picam2.post_callback = draw

picam2.start()

print("THIS WILL ONLY WORK IF WAYLAND IS USED")
print("IN RASPI CONFIG TURN ON WAYLAND INTEAD OF X")

while True:
  im = picam2.capture_array()
  cv2.imshow("Camera", im)
  # required to update screen
  cv2.waitKey(1)

time.sleep(60)
# do not use while true, it will slow down the FPS for some fuking reason