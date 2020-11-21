import cv2
import numpy as np

#create 3 separate BGRA images as our "layers"
layer1 = np.zeros((500, 500, 4))
layer2 = np.zeros((500, 500, 4))
layer3 = np.zeros((500, 500, 4))

#draw a red circle on the first "layer",
#a green rectangle on the second "layer",
#a blue line on the third "layer"
red_color = (0, 0, 255, 255)
green_color = (0, 255, 0, 255)
blue_color = (255, 0, 0, 255)
cv2.circle(layer1, (255, 255), 100, red_color, 5)
cv2.rectangle(layer2, (175, 175), (335, 335), green_color, 5)
cv2.line(layer3, (170, 170), (340, 340), blue_color, 5)

res = layer1[:] #copy the first layer into the resulting image

#copy only the pixels we were drawing on from the 2nd and 3rd layers
#(if you don't do this, the black background will also be copied)
cnd = layer2[:, :, 3] > 0
res[cnd] = layer2[cnd]
cnd = layer3[:, :, 3] > 0
res[cnd] = layer3[cnd]

cv2.imwrite("out.png", res)