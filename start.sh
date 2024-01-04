#!/usr/bin/bash
export DISPLAY=:0 
source ~/mp/bin/activate
python3 real_time_with_labels.py --model mobilenet_v2.tflite --label coco_labels.txt