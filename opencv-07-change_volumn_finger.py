from cv2 import cv2
import time
import hand as htm

pTime = 0

cap = cv2.VideoCapture(0)

detector = htm.handDetector(detectionCon = 1)

while True:
	ret, frame = cap.read()
	frame = detector.findHands(frame)
	lmList = detector.findPosition(frame, draw = False)

	if len(lmList) != 0:
		# print(lmList[4], lmList[8])

		# thumb coordinates
		x1, y1 = lmList[4][1], lmList[4][2]
		# index finger coordinates
		x2, y2 = lmList[8][1], lmList[8][2]

		# draw two circles on top of thumb finger and index finger
		cv2.circle(frame, (x1, y1), 10, (255, 0, 255), -1)
		cv2.circle(frame, (x2, y2), 10, (255, 0, 255), -1)

		# connect two circle with a line 
		cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

		# draw a circle at the center of line
		cx, cy = (x1 + x2)//2, (y1 + y2)//2
		cv2.circle(frame, (cx, cy), 10, (255, 0, 255), -1)


# Show FPS
	#Return the number of second 
	cTime = time.time()
	#calcule fps frames per second
	fps = 1/(cTime - pTime)
	pTime = cTime
	# print(type(fps))

	# show fps in window by text
	cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

# Show
	cv2.imshow("Window", frame)
	# wait in 1/1000s, exit if click q
	if cv2.waitKey(1) == ord("q"):
		break


cap.release()
cv2.destroyAllWindows()
