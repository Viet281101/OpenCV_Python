# Copyright 2020 The MediaPipe Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""MediaPipe Hands."""

import enum
from typing import NamedTuple

import numpy as np

# pylint: disable=unused-import
from mediapipe.calculators.core import constant_side_packet_calculator_pb2
from mediapipe.calculators.core import gate_calculator_pb2
from mediapipe.calculators.core import split_vector_calculator_pb2
from mediapipe.calculators.tensor import image_to_tensor_calculator_pb2
from mediapipe.calculators.tensor import inference_calculator_pb2
from mediapipe.calculators.tensor import tensors_to_classification_calculator_pb2
from mediapipe.calculators.tensor import tensors_to_detections_calculator_pb2
from mediapipe.calculators.tensor import tensors_to_landmarks_calculator_pb2
from mediapipe.calculators.tflite import ssd_anchors_calculator_pb2
from mediapipe.calculators.util import association_calculator_pb2
from mediapipe.calculators.util import detections_to_rects_calculator_pb2
from mediapipe.calculators.util import logic_calculator_pb2
from mediapipe.calculators.util import non_max_suppression_calculator_pb2
from mediapipe.calculators.util import rect_transformation_calculator_pb2
from mediapipe.calculators.util import thresholding_calculator_pb2
# pylint: enable=unused-import
from mediapipe.python.solution_base import SolutionBase
# pylint: disable=unused-import
from mediapipe.python.solutions.hands_connections import HAND_CONNECTIONS
# pylint: enable=unused-import

import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList


    def findDistance(self, p1, p2, img, draw=True):

        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length,img, [x1, y1, x2, y2, cx, cy]

    def fingersUp(self):
        fingers = []

        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


class HandLandmark(enum.IntEnum):
  """The 21 hand landmarks."""
  WRIST = 0
  THUMB_CMC = 1
  THUMB_MCP = 2
  THUMB_IP = 3
  THUMB_TIP = 4
  INDEX_FINGER_MCP = 5
  INDEX_FINGER_PIP = 6
  INDEX_FINGER_DIP = 7
  INDEX_FINGER_TIP = 8
  MIDDLE_FINGER_MCP = 9
  MIDDLE_FINGER_PIP = 10
  MIDDLE_FINGER_DIP = 11
  MIDDLE_FINGER_TIP = 12
  RING_FINGER_MCP = 13
  RING_FINGER_PIP = 14
  RING_FINGER_DIP = 15
  RING_FINGER_TIP = 16
  PINKY_MCP = 17
  PINKY_PIP = 18
  PINKY_DIP = 19
  PINKY_TIP = 20


_BINARYPB_FILE_PATH = 'mediapipe/modules/hand_landmark/hand_landmark_tracking_cpu.binarypb'


class Hands(SolutionBase):
  """MediaPipe Hands.
  MediaPipe Hands processes an RGB image and returns the hand landmarks and
  handedness (left v.s. right hand) of each detected hand.
  Note that it determines handedness assuming the input image is mirrored,
  i.e., taken with a front-facing/selfie camera (
  https://en.wikipedia.org/wiki/Front-facing_camera) with images flipped
  horizontally. If that is not the case, use, for instance, cv2.flip(image, 1)
  to flip the image first for a correct handedness output.
  Please refer to https://solutions.mediapipe.dev/hands#python-solution-api for
  usage examples.
  """

  def __init__(self,
               static_image_mode=False,
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
    """Initializes a MediaPipe Hand object.
    Args:
      static_image_mode: Whether to treat the input images as a batch of static
        and possibly unrelated images, or a video stream. See details in
        https://solutions.mediapipe.dev/hands#static_image_mode.
      max_num_hands: Maximum number of hands to detect. See details in
        https://solutions.mediapipe.dev/hands#max_num_hands.
      model_complexity: Complexity of the hand landmark model: 0 or 1.
        Landmark accuracy as well as inference latency generally go up with the
        model complexity. See details in
        https://solutions.mediapipe.dev/hands#model_complexity.
      min_detection_confidence: Minimum confidence value ([0.0, 1.0]) for hand
        detection to be considered successful. See details in
        https://solutions.mediapipe.dev/hands#min_detection_confidence.
      min_tracking_confidence: Minimum confidence value ([0.0, 1.0]) for the
        hand landmarks to be considered tracked successfully. See details in
        https://solutions.mediapipe.dev/hands#min_tracking_confidence.
    """
    super().__init__(
        binary_graph_path=_BINARYPB_FILE_PATH,
        side_inputs={
            'model_complexity': model_complexity,
            'num_hands': max_num_hands,
            'use_prev_landmarks': not static_image_mode,
        },
        calculator_params={
            'palmdetectioncpu__TensorsToDetectionsCalculator.min_score_thresh':
                min_detection_confidence,
            'handlandmarkcpu__ThresholdingCalculator.threshold':
                min_tracking_confidence,
        },
        outputs=[
            'multi_hand_landmarks', 'multi_hand_world_landmarks',
            'multi_handedness'
        ])

  def process(self, image: np.ndarray) -> NamedTuple:
    """Processes an RGB image and returns the hand landmarks and handedness of each detected hand.
    Args:
      image: An RGB image represented as a numpy ndarray.
    Raises:
      RuntimeError: If the underlying graph throws any error.
      ValueError: If the input image is not three channel RGB.
    Returns:
      A NamedTuple object with the following fields:
        1) a "multi_hand_landmarks" field that contains the hand landmarks on
           each detected hand.
        2) a "multi_hand_world_landmarks" field that contains the hand landmarks
           on each detected hand in real-world 3D coordinates that are in meters
           with the origin at the hand's approximate geometric center.
        3) a "multi_handedness" field that contains the handedness (left v.s.
           right hand) of the detected hand.
    """

    return super().process(input_data={'image': image})