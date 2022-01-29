from cv2 import cv2
import random

img = cv2.imread("1-Blue_320x180.png", 1)


print(img)
print(type(img))
# (180, 320, 3) size of image and chanel
print(img.shape)


# for i in range(100):
# 	for j in range(img.shape[1]):
# 		img[i][j] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

# To cut and paste a zone in image:
choseZone = img[0:30, 50:90]
img[100:130, 100:140] = choseZone

# Change the scale of window
img = cv2.resize(img, (0,0), fx = 3.0, fy = 3.0)

# Show
cv2.imshow("Image", img)

# For closing the window if click any key
cv2.waitKey()
