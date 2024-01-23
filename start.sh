#!/usr/bin/bash
echo run this using: bash start.sh
export DISPLAY=:0 
source ~/mp/bin/activate

python3 real_time_with_labels_with_serial.py --model mobilenet_v2.tflite --label coco_labels.txt