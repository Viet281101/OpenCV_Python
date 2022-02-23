
import cv2
import cvzone

# Use the webcam
cap = cv2.VideoCapture(0)

### Or you can see the blink in my video here
# cap = cv2.VideoCapture('webcam_video_blink.mp4')


while True:
	success, img = cap.read()

	# change the screen size
	img = cv2.resize(img, (640, 420))

	# Show
	cv2.imshow("Window", img)
	# wait in 1/1000s, exit if click q
	if cv2.waitKey(1) == ord("q"):
		break


cap.release()
cv2.destroyAllWindows()

