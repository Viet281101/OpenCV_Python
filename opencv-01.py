from cv2 import cv2

# read image
img = cv2.imread("1-Blue_320x180.png", 1)


# resize image
# img = cv2.resize(img, (640, 360))
# img = cv2.resize(img, (0,0), fx = 3.0, fy = 3.0)


# rotate image
# img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
# img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)


# output
cv2.imshow("space", img)
k = cv2.waitKey()


# print number of character from ascii table
# print(k)
# print(ord("s"))


#save to new file if click 's' 
if k == ord("s"):
	cv2.imwrite("new_image.jpg", img)


