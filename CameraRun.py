import time
import picamera
import numpy as np
from PIL import Image
# Create an array representing a 1280x720 image of
# a cross through the center of the display. The shape of
# the array must be of the form (height, width, color)
a = np.zeros((2400,3200 , 3), dtype=np.uint8)
a[240, :, :] = 0xff
a[:, 320, :] = 0xff

img = Image.open('out.png')

pad = Image.new('RGBA',(
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
        ))
        
pad.paste(img, (0, 0),img)




camera = picamera.PiCamera()
camera.resolution = (3200,2400)
camera.rotation = 90
camera.framerate = 24
camera.hflip = True
o = camera.add_overlay(pad.tobytes(),size=img.size, layer=3,alpha=0.5)
camera.start_preview(fullscreen=False,window=(0,0,320,240)) #
# Add the overlay directly into layer 3 with transparency;
# we can omit the size parameter of add_overlay as the
# size is the same as the camera's resolution

try:
    # Wait indefinitely until the user terminates the script
    while True:
        time.sleep(1)
finally:
    camera.remove_overlay(o)
    pass