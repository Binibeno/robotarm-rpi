#!/usr/bin/python3

# Copyright (c) 2022 Raspberry Pi Ltd
# Author: Alasdair Allan <alasdair@raspberrypi.com>
# SPDX-License-Identifier: BSD-3-Clause

# A TensorFlow Lite example for Picamera2 on Raspberry Pi OS Bullseye
#
# Install necessary dependences before starting,
#
# $ sudo apt update
# $ sudo apt install build-essential
# $ sudo apt install libatlas-base-dev
# $ sudo apt install python3-pip
# $ pip3 install tflite-runtime
# $ pip3 install opencv-python==4.4.0.46
# $ pip3 install pillow
# $ pip3 install numpy
#
# and run from the command line,
# $ source ~/mp/bin/activate
# $ python3 real_time_with_labels.py --model mobilenet_v2.tflite --label coco_labels.txt

import serial
import serial.tools.list_ports

import os
# fix camera on ssh 
os.environ["DISPLAY"] = ":0"

import time
import argparse

import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

from picamera2 import MappedArray, Picamera2, Preview

normalSize = (640, 480)
lowresSize = (320, 240)

rectangles = []

def sysprint(a):
    print('\033[92m' + "SYS: " +'\033[0m' + str(a))

def init_serial():
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    sysprint(ports)
    
    
    
    if (ports.__len__() == 0):
        sysprint("No ports available")
        exit()
    
    port = ports[0]
    
    global ser
    #  countiously read port and print data
    ser = serial.Serial(port, 9600, timeout=1)
    ser.close()
    ser.open()
    while True:
        # read_val = ser.read(size=64)
        # if (read_val != '' )and (read_val != b''):
        #     read_val = read_val.decode('utf-8')
        #     print(read_val)
        # time.sleep(0.1)
    
        #  read serial line by line
        line = ser.readline()
        if (line != '' )and (line != b''):
            nice = line.decode('utf-8')
            print("COM: " + nice)
            if (line == b'READY\r\n'):
                sysprint("Arm Ready. Start sending commands.")
                break
            
            
            
    ser.write(b"m1090\r\n")
    time.sleep(0.001)
    
    ser.write(b"m2040\r\n")
    time.sleep(0.001)
    
    ser.write(b"m0100\r\n")
    time.sleep(0.001)
    
    ser.write(b"u\r\n")


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def ReadLabelFile(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    ret = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret

def current_milli_time():
    return round(time.time() * 1000)

lastMove = 0;

def DrawRectangles(request):
    with MappedArray(request, "main") as m:
        # x min = 0 in the most left side of the image
        # x max = 320 in the most left side of the image

        # y min = 0 at the top of the image
        # y max = 240 at the bottom of the image
        # rectangles = [[10, 10, 310, 230]]

        if len(rectangles) == 1:

             # rect y center
            rect_y_center = (rectangles[0][1] + rectangles[0][3]) / 2
            # rect x center
            rect_x_center = (rectangles[0][0] + rectangles[0][2]) / 2


            # map x and y to 0-320 to 40-140
            arm_rot = map_range(rect_x_center, 0, 320, 40, 140)
            pad_rot = str(arm_rot).rjust(3, "0")
            sysprint(pad_rot)
            command = "m0" + pad_rot + "\r\n"
            bytes = str.encode(command)

            global lastMove
            if (current_milli_time() - lastMove > 500):
                lastMove = current_milli_time()
                ser.write(bytes)

                time.sleep(0.001)

                ser.write(b"u\r\n")
                time.sleep(0.001)

            

            

        for rect in rectangles:

            #  rect = [xmin, ymin, xmax, ymax]

            # print(rect[2])

            # calculate center

            # rect y center
            rect_y_center = (rect[1] + rect[3]) / 2
            # rect x center
            rect_x_center = (rect[0] + rect[2]) / 2

            # magick?
            c_rect_start = (int((rect_x_center -5) * 2) - 5, int((rect_y_center-5) * 2) - 5)
            c_rect_end = (int((rect_x_center+5) * 2) + 5, int((rect_y_center+5) * 2) + 5)
            cv2.rectangle(m.array, c_rect_start, c_rect_end, (255, 0, 0, 0))


            rect_start = (int(rect[0] * 2) - 5, int(rect[1] * 2) - 5)
            rect_end = (int(rect[2] * 2) + 5, int(rect[3] * 2) + 5)
            # print(rect_start,rect_end)
            cv2.rectangle(m.array, rect_start, rect_end, (0, 255, 0, 0))
            if len(rect) == 5:
                text = rect[4]
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(m.array, text, (int(rect[0] * 2) + 10, int(rect[1] * 2) + 10),
                            font, 1, (255, 255, 255), 2, cv2.LINE_AA)


def InferenceTensorFlow(image, model, output, label=None):
    global rectangles

    if label:
        labels = ReadLabelFile(label)
    else:
        labels = None

    interpreter = tflite.Interpreter(model_path=model, num_threads=4)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    # 300 x 300
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = False
    if input_details[0]['dtype'] == np.float32:
        floating_model = True

    rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    initial_h, initial_w, channels = rgb.shape

    picture = cv2.resize(rgb, (width, height))

    input_data = np.expand_dims(picture, axis=0)
    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    detected_boxes = interpreter.get_tensor(output_details[0]['index'])
    detected_classes = interpreter.get_tensor(output_details[1]['index'])
    detected_scores = interpreter.get_tensor(output_details[2]['index'])
    num_boxes = interpreter.get_tensor(output_details[3]['index'])

    rectangles = []
    for i in range(int(num_boxes)):
        top, left, bottom, right = detected_boxes[0][i]
        classId = int(detected_classes[0][i])
        score = detected_scores[0][i]
        if score > 0.5:
            xmin = left * initial_w
            ymin = bottom * initial_h
            xmax = right * initial_w
            ymax = top * initial_h
            box = [xmin, ymin, xmax, ymax]
            rectangles.append(box)
            if labels:
                print(labels[classId], 'score = ', score)
                rectangles[-1].append(labels[classId])
            else:
                print('score = ', score)


def main():
    parser = argparse.ArgumentParser()
    #! add require=true
    parser.add_argument('--model', help='Path of the detection model.')
    parser.add_argument('--label', help='Path of the labels file.')
    parser.add_argument('--output', help='File path of the output image.')
    args = parser.parse_args()

    if (args.output):
        output_file = args.output
    else:
        output_file = 'out.jpg'

    if (args.label):
        label_file = args.label
    else:
        label_file = None

    print("TEMPORARY OVERWRITE FOR MODEL FILE")
    args.model="mobilenet_v2.tflite"


    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)
    config = picam2.create_preview_configuration(main={"size": normalSize},
                                                 lores={"size": lowresSize, "format": "YUV420"})
    picam2.configure(config)


    # stride's value is 320, same as in the x coordinate of the lores mode
    # (this function basicly gets that value)
    stride = picam2.stream_configuration("lores")["stride"]
    picam2.post_callback = DrawRectangles

    picam2.start()

    sysprint("Starting Serial...")
    init_serial()

    while True:
        buffer = picam2.capture_buffer("lores")
        grey = buffer[:stride * lowresSize[1]].reshape((lowresSize[1], stride))
        _ = InferenceTensorFlow(grey, args.model, output_file, label_file)
        # time.delay(100)



if __name__ == '__main__':
    main()

