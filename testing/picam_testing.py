from picamera2 import MappedArray, Picamera2, Preview

import os
# fix camera on ssh 
os.environ["DISPLAY"] = ":0"

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

normalSize = (800, 600)

config = picam2.create_preview_configuration(main={"size": normalSize},
                                                 )
picam2.configure(config)

picam2.start()

while True: 
  pass