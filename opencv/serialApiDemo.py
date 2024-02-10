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


print("Starting serial communcation")
ser = serialapi.init_serial()



# min: 14.5
# max: 43.5
# unit: cm
r = 43.5



# move to radius
# serialapi.armToCM(ser, r, False)
# time.sleep(0.001)

serialapi.moveMotor(ser, 5, 73)
serialapi.updateMotor(ser)

time.sleep(1)


serialapi.moveMotor(ser, 5, 10)
serialapi.updateMotor(ser)
