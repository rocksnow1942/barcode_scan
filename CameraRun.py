import time
import picamera
import numpy as np

# Create an array representing a 1280x720 image of
# a cross through the center of the display. The shape of
# the array must be of the form (height, width, color)
a = np.zeros((2400,3200 , 3), dtype=np.uint8)
a[240, :, :] = 0xff
a[:, 320, :] = 0xff

camera = picamera.PiCamera()
camera.resolution = (3200,2400)
camera.rotation = 90
camera.framerate = 24
camera.hflip = True
camera.start_preview(fullscreen=False,window=(0,0,320,240)) #
# Add the overlay directly into layer 3 with transparency;
# we can omit the size parameter of add_overlay as the
# size is the same as the camera's resolution
o = camera.add_overlay(a, layer=3, alpha=64,)
try:
    # Wait indefinitely until the user terminates the script
    while True:
        time.sleep(1)
finally:
    camera.remove_overlay(o)
    pass