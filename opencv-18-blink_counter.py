
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot


### Use the webcam
cap = cv2.VideoCapture(0)

### Or you can see the blink in my video here
# cap = cv2.VideoCapture('webcam_video_blink.mp4')


detector = FaceMeshDetector(maxFaces = 1)

plotY = LivePlot(640, 480, [20, 50])

idlist = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]


while True:

	if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
		cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

	success, img = cap.read()

	img, faces = detector.findFaceMesh(img, draw = False)


	if faces:
		face = faces[0]
		for id in idlist:
			cv2.circle(img, face[id], 5, (255, 0, 255), cv2.FILLED)

		left_Up = face[159]
		left_Down = face[23]
		left_Left = face[130]
		left_Right = face[243]

		length_Ver, _ = detector.findDistance(left_Left, left_Right) 
		length_Hor, _ = detector.findDistance(left_Up, left_Down)
		
		cv2.line(img, left_Up, left_Down, (0, 200, 0), 3)
		cv2.line(img, left_Left, left_Right, (0, 200, 0), 3)
		
		ratio = int((length_Ver / length_Hor) * 10)


		imgPlot = plotY.update(ratio)

		# change the screen size
		img = cv2.resize(img, (640, 480))
		

		# show plot window
		# cv2.imshow("Window Plot", imgPlot)

		
		imgStack = cvzone.stackImages([img, imgPlot], 2, 1)

	else:
		img = cv2.resize(img, (640, 480))
		imgStack = cvzone.stackImages([img, img], 2, 1)



	# Show main window
	cv2.imshow("Window", imgStack)

	
	if cv2.waitKey(25) == ord("q"):
		break


cap.release()
cv2.destroyAllWindows()

