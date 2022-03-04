
# import packages
import cv2
import matplotlib.pyplot as plt


# load sample image
image = cv2.imread("images/selfie_picture.jpg")


# display loaded image
plt.title('Original Image')
plt.imshow(image)


# crop image
cropped = image[100:1200, 0:1500]


# display cropped image
plt.title('Cropped Image')
plt.imshow(cropped)
