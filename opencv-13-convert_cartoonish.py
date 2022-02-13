import cv2
import numpy as np


img = cv2.imread("selfie_picture.jpg")

# Because my picture is too big so I resize it:
img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.medianBlur(gray, 5)

edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 5)

color = cv2.bilateralFilter(img, 9, 250, 250)

cartoon = cv2.bitwise_and(color, color, mask = edges)



cv2.imshow("show", cartoon)

#save the cartoon picture to folder if click 's' 
if cv2.waitKey() == ord("s"):
	cv2.imwrite("your_cartoon_picture.jpg", cartoon)

cv2.waitKey(0)
cv2.destroyAllWindows()

