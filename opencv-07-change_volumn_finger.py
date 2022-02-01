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
