# TL:DR
Object tracking robotic arm. My presentation sums up most of what this project is about. Look at my website for more (up to date) info.

Links: 
- Presentation: https://1drv.ms/p/s!Auo1wIU3YBEcir1iVWpIdz-QKitpkA
- Site: https://binibeno.hu/projects/robotarm/info/
- Contact: https://binibeno.hu/about/

# Intro

The information here will be pretty technical. I wrote most of the documentation just for myself. 

If this is your first time stumbling upon my project I recommend looking at my website at my presentation first :
[available on OneDrive with this link](https://1drv.ms/p/s!Auo1wIU3YBEcir1iVWpIdz-QKitpkA).

The links mentioned in the presentation are the followings: (These are kept up to date): [Documentation](https://binibeno.hu/projects/robotarm/info/) and [Interactive](https://binibeno.hu/projects/robotarm/)


If you have any question, would like to try out the code or just interested in my project, feel free to contact me. Email is on my [website's about page](https://binibeno.hu/about/). 

**My final creation can be seen in the OpenCV direactory. Take a look at that directory's README for more info.** 

# Technical information

Some more technical information (mostly for myself can be found down below.)
Some of the resources could be useful for you as well if you are working with
- raspberry pi (4B) and its camera
- opencv based computer vision in python
- serial communication in python (multithreaded)
-  **easy** to use algorithm for calculating arm angles for robotic arm controls 


## Project related


### Before you begin, you need to set up your Raspberry Pi with Raspberry 64-bit Pi OS (preferably updated to Buster).

What libraries are used?
For computer vision: 
- opencv 
- picamera2 (newer picamera)

For AI:
- Tensorflow (Lite) and Mediapipe

## **Important!! Set up python venv**
Was useful (for libcamera2, opencv and mediapipe): Set up venv in Python  
--system-site-packages flag is very important for picamera2 to work! 
https://github.com/raspberrypi/picamera2/issues/503

`python3 -m venv ~/mp --system-site-packages`
(to activate `source ~/mp/bin/activate`)

See more in Tensorflow install gist.

## Tensorflow and Mediapipe

See install info from https://gist.github.com/Binibeno/61ae0e4fa730402714cbebe7d24436de

Activate virtual env before using!!: source ~/mp/bin/activate

In vscode set python binary to: /home/admin/mp/bin/python

## Picamera 2

https://www.raspberrypi.com/documentation/computers/camera_software.html

https://github.com/raspberrypi/picamera2

https://datasheets.raspberrypi.com/camera/raspberry-pi-camera-guide.pdf


"Picamera2 is only supported on Raspberry Pi OS Bullseye (or later) images, both 32 and 64-bit. As of September 2022, Picamera2 is pre-installed on images downloaded from Raspberry Pi. It works on all Raspberry Pi boards right down to the Pi Zero, although performance in some areas may be worse on less powerful devices."

To test rpi cam: 
`rpicam-hello -t 0`

Download examples from: https://github.com/raspberrypi/picamera2/tree/main/examples

(much of my code in the camTesting folder are based on these examples)

Last updated: 2024. 05. 21. \
Benedek Nemeth