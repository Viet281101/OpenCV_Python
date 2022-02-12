import cv2
import mediapipe as mp
import time


mp_objecttron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)


with mp_objecttron.Objectron(static_image_mode = False, 
							max_num_objects = 2, 
							min_detection_confidence = 0.5, 
							min_tracking_confidence = 0.8, 
							model_name = 'Cup') as objectron:

	while cap.isOpened():

		success, image = cap.read()

		start = time.time()

		# Convert the BGR image to RGB
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# To improve performance, optionally mark the image as not writeable to pass by reference
		image.flags.writeable = False
		results = objectron.process(image)

		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


		if results.detected_objects:
			for detected_objects in results.detected_objects:
				mp_drawing.draw_landmarks(image, detected_objects.landmarks_2d, mp_objecttron.BOX_CONNECTIONS)
				mp_drawing.draw_axis(image, detected_objects.rotation, detected_objects.translation)



		end = time.time()
		totalTime = end - start

		fps = 1 / totalTime

		cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)


		cv2.imshow('MediaPipe Objectron', image)

		
		key = cv2.waitKey(5)
		if key == ord('q'):
			break


cap.release()
cv2.destroyAllWindows()



