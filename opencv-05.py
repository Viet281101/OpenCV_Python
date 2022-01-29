from cv2 import cv2

cap = cv2.VideoCapture('webcam_video.mp4')

while True:
	ret, frame = cap.read()
	# print(ret)
	width = int(cap.get(3))
	height = int(cap.get(4))

	# Draw the lines:
	# black line
	img = cv2.line(frame, (0, 0), (width, height), (0, 0, 0), 25)

	# white line
	img = cv2.line(frame, (0, height), (width, 0), (255, 255, 255), 25)


	# Draw a rectangle
	# img = cv2.rectangle(frame, (100, 100), (400, 400), (0, 0, 0), 25)
	img = cv2.rectangle(frame, (100, 100), (400, 400), (0, 0, 0), -1)

	cv2.imshow("Window", frame)
	# cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
	if cv2.waitKey(1) == ord("q"):
		break

	# Change the scale of window
	img = cv2.resize(img, (0,0), fx = 3.0, fy = 3.0)

cap.release()
cap.destroyAllWindows()
