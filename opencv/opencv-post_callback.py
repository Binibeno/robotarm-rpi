import os
os.environ["DISPLAY"] = ":0"




import time

import numpy as np
import cv2
from picamera2 import Picamera2, Preview,MappedArray

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(queue=False))
picam2.start_preview(Preview.QTGL)


# inbuilt overlay function of picamera2
# overlay = np.zeros((300, 400, 4), dtype=np.uint8)
# overlay[:150, 200:] = (255, 0, 0, 64)
# overlay[150:, :200] = (0, 255, 0, 64)
# overlay[150:, 200:] = (0, 0, 255, 64)
# picam2.set_overlay(overlay)



# called after every frame
def draw(request):
    with MappedArray(request, "main") as m:
      print("callled")
      # m.array is the input image for opencv functions
      # -1 fills in the rect.
      img = np.zeros([100,100,3],dtype=np.uint8)
      img.fill(255) # or img[:] = 255
      cv2.rectangle(img, (30, 50), (70, 90), (0, 255, 0, 0), -1)
      m.array = img


# callback - here I can use opencv
picam2.post_callback = draw

picam2.start()
time.sleep(1)

time.sleep(2)
