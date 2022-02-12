import cv2
import mediapipe as mp
import time


mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)


with mp_holistic.Holistic(min_detection_confidence = 0.5, 
							min_tracking_confidence = 0.5) as holistic:

	while cap.isOpened():
		
		success, image = cap.read()

		start = time.time()


		# Flip the image horizontally for a later selfie-view display
		# COnvert the BGR image to RGB.
		image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

		# To improve performance, optionally mark the image as not writeable to pass by reference.
		image.flags.writeable = False


		# Process the image and detect the holistic
		results = holistic.process(image)


		# Draw landmark annotation on the image
		image.flags.writeable = True


		# Convert the image color back so it can be displayed
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


		# print(results.pose_landmarks)

		# FACE_CONNECTIONS seems to be renamed/replaced by FACEMESH_TESSELATION
		# PS: If you want just the outlines of the face, it's now FACEMESH_CONTOURS
		mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)

		mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
		mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
		mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

		end = time.time()
		totalTime = end - start

		fps = 1 / totalTime
		# print("FPS: ", fps)

		cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)


		cv2.imshow('MediaPipe Objectron', image)

		key = cv2.waitKey(5)
		if key == ord('q'):
			break


cap.release()
cv2.destroyAllWindows()




