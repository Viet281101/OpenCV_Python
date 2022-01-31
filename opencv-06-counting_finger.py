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

while True:
	ret, frame = cap.read()
	frame = detector.findHands(frame)
	# find the position of 20 point in your hand
	lmList = detector.findPosition(frame, draw = False)
	# print(lmList)


	if len(lmList) != 0:
		# for the most long finger

		if lmList[8][2] < lmList[6][2]:
			print("The first finger is open")


	h, w, c = lst_2[0].shape
	frame[0:h, 0:w] = lst_2[0]


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

