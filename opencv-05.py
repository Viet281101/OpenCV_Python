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
	img = cv2.rectangle(frame, (100, 100), (200, 200), (0, 0, 0), -1)

# Draw a circle
	img = cv2.circle(frame, (400, 400), 50, (125, 24, 78), -1)

# Write a text
	font = cv2.FONT_HERSHEY_TRIPLEX
	img = cv2.putText(frame, "banana eating cherry", (0, height - 400), font, 2, 4)


# Show
	cv2.imshow("Window", frame)
	# cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
	if cv2.waitKey(1) == ord("q"):
		break


cap.release()
cap.destroyAllWindows()
