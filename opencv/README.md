# My creations to note: 
- opencv-post_callback.py: This is a minimal example of using the post_callback to draw on the preview window.
- opencv-select-color.py: Will only show bright green colored objects on a solid white background. (source: https://stackoverflow.com/a/53989391/13167888)
- cv-select-color-with-border.py: select-color rewritten, gets coords and display a border around the object. (see: https://stackoverflow.com/q/59334191/13167888)
- cv-color-serial.py: move the robotarm based on colors. **LATEST**
All examples named are available in the examples directory. Online: https://github.com/raspberrypi/picamera2/tree/main/examples
Full docs: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

# How to setup
Follow this guide: https://gist.github.com/Binibeno/61ae0e4fa730402714cbebe7d24436de

# How to run examples (even with ssh!)
Run this using `bash`!
```
export DISPLAY=:0 
source ~/mp/bin/activate
```
Then run your code.

I also recommend adding this piece of code to every camere-using python file:
```
import os
os.environ["DISPLAY"] = ":0"
```
This will fix the preview window on ssh, if you forgot to do it beforehand. 

# Dev IDE setup
I use vscode on my laptop, and use the remote ssh extension to connect to the pi.
I've also created a workspace with 2 folders (located at different paths) added to it. One of them are the example from the github repo above, the other is my own code (and repo).

# How not to kill your camera!
- Static electricity can kill the camera. No joke. Touch something metal before touching the camera. **The camera runs at a really low voltage!**
- NEVER unplug or even mess around with the connector while the raspberry pi has power. Even when the raspberry pi is off. Disconnect from all power (even monitor!) before messing with the connector. Negative and positive terminals are right next to each other and can easily short out.
- Camera cable extremely susceptible to interference. Don't run it next to power cables, even the pi's power cable. **DO NOT COIL THE CABLE!! IT WILL CAUSE INTERFERENCE!!**

# FAQ
### How to switch from preview res to full res: See file switch_mode.py

### How to start preview
```
from picamera2 import Picamera2, Preview,MappedArray

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())

picam2.start_preview(Preview.QTGL)
```
see: preview.py, previw

# How to overlay things
With picamera2 and post processing (like adding rectangles and text) there are multiple options. 

## Option 1: Picamera's built in preview has *basic* overlay capabilities
It can basicly only be used to draw rectangles and text.
See example files: overlay_gl.py, overlay_qt.py
**IMPORTANT**: The `Preview.QTGL` preview mode's preformance is way better because it uses 3d acceleration. The `Preview.QT` preview mode is slow and not recommended.

## Option 2: pre_callback and post_callback
These are 2 functions that can be used with the preview window. `pre_callback` is called before the image is passed to any video encoders. `post_callback` is called after the image is passed to the video encoders. These functions can be used to draw on the image. See example files: opencv_face_detect_3.py, timestamped_video.py
**IMPORTANT**: Only a small bit of processing should be done, otherwise frames can be dropped. If you need to do more processing, use other options. 

See example: opencv_face_detect_2.py
See: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf (Sections Application Notes > Manipulate camera buffers in place 9.4, Page 69)

Note
- If you use this option for doing the light processing in the post_callback (like adding a drawing a box), and use a While loop to the heavy processing (like identifying faces), the best perfomance is achived. The preview window (and post_callback) will run in 30 fps, while the heavy processing will lag behind. Do read the documentation!! 

## Option 3: Use opencv to display preview windows
See: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf (Sections Application Notes > Manipulate camera buffers in place 9.4, Page 69)

Notes: Worse performance than option 2 or 1, but WAY more options. 
See example: opencv_face_detect.py -- This is the only offical example that uses opencv to display the preview window.

My minimal example: 
```
import cv2
from picamera2 import Picamera2
face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()
picam2 = Picamera2()
# not the max resolution
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (800 , 600 )}))
picam2.start()

while True:
    im = picam2.capture_array()
    cv2.imshow("Camera", im)
    cv2.waitKey(1)

```

**IMPORTANT: The format is important, converting between requires lots of processing.**
**IMPORTANT: This only works with Wayland, not X. You can change this settings in raspi-config.**
