
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector


### Use the webcam
cap = cv2.VideoCapture(0)

### Or you can see the blink in my video here
# cap = cv2.VideoCapture('webcam_video_blink.mp4')


detector = FaceMeshDetector(maxFaces = 1)


idlist = [22, 23, 24]


while True:

	if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
		cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

	success, img = cap.read()

	img, faces = detector.findFaceMesh(img, draw = False)


	if faces:
		face = faces[0]
		for id in idlist:
			cv2.circle(img, face[id], 5, (255, 0, 255), cv2.FILLED)


	# change the screen size
	img = cv2.resize(img, (640, 480))


	# Show
	cv2.imshow("Window", img)

	# wait in 1/1000s, exit if click q
	if cv2.waitKey(1) == ord("q"):
		break


cap.release()
cv2.destroyAllWindows()

