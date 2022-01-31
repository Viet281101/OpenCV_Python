from cv2 import cv2
import time
import os
import hand as htm

pTime = 0
cap = cv2.VideoCapture(0)

FolderPath = "Fingers"
lst = os.listdir(FolderPath)
lst_2 = []

for i in lst:
	image = cv2.imread(f"{FolderPath}/{i}")
	# print(f"{FolderPath}/{i}")
	lst_2.append(image)

# print(lst_2[0].shape)

detector = htm.handDetector(detectionCon = 1)

# Id of top point of 5 finger in your hand
fingerid = [4, 8, 12, 16, 20]

while True:
	ret, frame = cap.read()
	frame = detector.findHands(frame)
	# find the position of 20 point in your hand
	lmList = detector.findPosition(frame, draw = False)
	# print(lmList)


	if len(lmList) != 0:
		fingers = []

		# for the thumb finger
		if lmList[fingerid[0]][1] < lmList[fingerid[0] - 2][1]:
			fingers.append(1)
		else:
			fingers.append(0)

		# for the 4 long finger
		for id in range(1, 5):

			if lmList[fingerid[id]][2] < lmList[fingerid[id] - 2][2]:
				fingers.append(1)
			else:
				fingers.append(0)
		
		# print(fingers)
		number_finger = fingers.count(1)
		# print(number_finger)
		# print(type(number_finger))


	h, w, c = lst_2[0].shape
	frame[0:h, 0:w] = lst_2[0]

	# draw a rectangle to affiche the number of finger
	cv2.rectangle(frame, (0, 125), (107, 240), (0, 255, 0), -1)
	cv2.putText(frame, str(number_finger, (20, 225), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 0), 5)


# Show FPS
	#Return the number of second 
	cTime = time.time()
	#calcule fps frames per second
	fps = 1/(cTime - pTime)
	pTime = cTime
	# print(type(fps))

	# show fps in window by text
	cv2.putText(frame, f"FPS: {int(fps)}", (150, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)



# Show
	cv2.imshow("Window", frame)
	# wait in 1/1000s, exit if click q
	if cv2.waitKey(1) == ord("q"):
		break


cap.release()
cv2.destroyAllWindows()

