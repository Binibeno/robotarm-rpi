import os
os.environ["DISPLAY"] = ":0"


import time

import numpy as np
import cv2
from picamera2 import Picamera2, Preview,MappedArray

picam2 = Picamera2()

preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (800 , 600 )})
picam2.configure(preview_config)


cv2.startWindowThread()


# called after every frame
def draw(request):
    with MappedArray(request, "main") as m:
      # m.array is the input image for opencv functions
      # -1 fills in the rect.
      # cv2.rectangle(m.array, (30, 50), (70, 90), (0, 255, 0, 0), -1)

      # convert to HSV
      hsv = cv2.cvtColor(m.array, cv2.COLOR_BGR2HSV) 
      # set lower and upper color limits
      lower_val = np.array([50,100,170])
      upper_val = np.array([70,255,255])
      # Threshold the HSV image to get only green colors
      mask = cv2.inRange(hsv, lower_val, upper_val)
      # apply mask to original image - this shows the green with black blackground
      only_green = cv2.bitwise_and(m.array,m.array, mask= mask)

      # create a black image with the dimensions of the input image
      background = np.zeros(m.array.shape, m.array.dtype)
      # invert to create a white image
      background = cv2.bitwise_not(background)
      # invert the mask that blocks everything except green -
      # so now it only blocks the green area's
      mask_inv = cv2.bitwise_not(mask)
      # apply the inverted mask to the white image,
      # so it now has black where the original image had green
      masked_bg = cv2.bitwise_and(background,background, mask= mask_inv)
      # add the 2 images together. It adds all the pixel values, 
      # so the result is white background and the the green from the first image
      final = cv2.add(only_green, masked_bg)


def selectByColor(img): 
  # convert to HSV
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
  # set lower and upper color limits
  lower_val = np.array([50,100,170])
  upper_val = np.array([70,255,255])
  # Threshold the HSV image to get only green colors
  mask = cv2.inRange(hsv, lower_val, upper_val)
  # apply mask to original image - this shows the green with black blackground
  only_green = cv2.bitwise_and(img,img, mask= mask)

  # create a black image with the dimensions of the input image
  background = np.zeros(img.shape, img.dtype)
  # invert to create a white image
  background = cv2.bitwise_not(background)
  # invert the mask that blocks everything except green -
  # so now it only blocks the green area's
  mask_inv = cv2.bitwise_not(mask)
  # apply the inverted mask to the white image,
  # so it now has black where the original image had green
  masked_bg = cv2.bitwise_and(background,background, mask= mask_inv)
  # add the 2 images together. It adds all the pixel values, 
  # so the result is white background and the the green from the first image
  final = cv2.add(only_green, masked_bg)
  return final


# callback - here I can use opencv
# picam2.post_callback = draw

picam2.start()

while True:
  img = picam2.capture_array()
  # convert to HSV
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
  # set lower and upper color limits
  lower_val = np.array([50,100,170])
  upper_val = np.array([70,255,255])
  # Threshold the HSV image to get only green colors
  mask = cv2.inRange(hsv, lower_val, upper_val)
  # apply mask to original image - this shows the green with black blackground
  only_green = cv2.bitwise_and(img,img, mask= mask)

  # create a black image with the dimensions of the input image
  background = np.zeros(img.shape, img.dtype)
  # invert to create a white image
  background = cv2.bitwise_not(background)
  # invert the mask that blocks everything except green -
  # so now it only blocks the green area's
  mask_inv = cv2.bitwise_not(mask)
  # apply the inverted mask to the white image,
  # so it now has black where the original image had green
  masked_bg = cv2.bitwise_and(background,background, mask= mask_inv)
  # add the 2 images together. It adds all the pixel values, 
  # so the result is white background and the the green from the first image
  final = cv2.add(only_green, masked_bg)


  cv2.imshow("Camera", final)
  # required to update
  cv2.waitKey(1)


time.sleep(60)
# do not use while true, it will slow down the FPS for some fuking reason