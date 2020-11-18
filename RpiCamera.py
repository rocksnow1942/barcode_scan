"""
How to setup:
# use sudo apt install python3-picamera.
adjust picamera v2 lense focus.
counter-clockwise if near focus, clockwise if further focus. 
max resolution is 3280×2464 
distance between focus plane and camera: 11mm. 
"""
import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (3280,2464)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    camera.capture('foo.jpg')



# capture to PIL
import io
import time
import picamera
from PIL import Image

# Create the in-memory stream
stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')
# "Rewind" the stream to the beginning so we can read its content
stream.seek(0)
image = Image.open(stream)