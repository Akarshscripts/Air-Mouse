"""
This module contains the detector class for the application which is built using MediaPipe.
"""

# 1st party imports
from typing import Optional

# 3rd party imports
import numpy as np
import mediapipe as mp

# local imports
from detector.models import HandDetectionResult
from detector.models import HandCoordinates, Hand, Cordinates
from config import MAX_NUM_HANDS, MIN_DETECTION_CONFIDENCE, MIN_TRACKING_CONFIDENCE


class Detector:

    def __init__(self):

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        # Create a Hands object
        self.hands_detector = self.mp_hands.Hands(
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )

        # indexes of the landmarks
        self.INDEX_FINGER_TIP = 8
        self.MIDDLE_FINGER_TIP = 12
        self.THUMB_TIP = 4
        self.WRIST = 0
        self.PINKY_TIP = 20

    def detect_hands(self, image: np.ndarray) -> HandDetectionResult:
        """
        This method is used to process the image and detect hands.
        This function returns the HandDetectionResult object which contains the following attributes:
            - multi_handedness: Optional[List[ClassificationList]]
            - multi_hand_landmarks: Optional[List[NormalizedLandmarkList]]
            - multi_hand_world_landmarks: Optional[List[NormalizedLandmarkList]]

        Args:
            image: The image to process.

        Returns:
            result: HandDetectionResult object
        """

        # process the image
        result = self.hands_detector.process(image)

        # return the result
        return HandDetectionResult(
            multi_hand_landmarks=result.multi_hand_landmarks,
            multi_handedness=result.multi_handedness,
            multi_hand_world_landmarks=result.multi_hand_world_landmarks,
        )

    def get_cordinates(
        self, results: HandDetectionResult, image: np.ndarray
    ) -> Optional[HandCoordinates]:
        """
        This method is used to get the cordinates of the index, middle and thumb tips.

        Args:
            results: The results object from the detector.
            image: The image to process.

        Returns:
            HandCoordinates: The cordinates of the provided landmark.
        """

        # check if the results are not none
        if not results.multi_hand_landmarks:
            return None

        # create empty cords
        left_hand_cordinates = None
        right_hand_cordinates = None

        # get the cordinates of the index, middle and thumb tips
        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks, results.multi_handedness
        ):

            # get the x and y cordinates of the index finger tip
            index_finger_tip_x = int(hand_landmarks.landmark[self.INDEX_FINGER_TIP].x * image.shape[1])
            index_finger_tip_y = int(hand_landmarks.landmark[self.INDEX_FINGER_TIP].y * image.shape[0])

            # get the x and y cordinates of the middle finger tip
            middle_finger_tip_x = int(hand_landmarks.landmark[self.MIDDLE_FINGER_TIP].x * image.shape[1])
            middle_finger_tip_y = int(hand_landmarks.landmark[self.MIDDLE_FINGER_TIP].y * image.shape[0])

            # get the x and y cordinates of the thumb tip
            thumb_tip_x = int(hand_landmarks.landmark[self.THUMB_TIP].x * image.shape[1])
            thumb_tip_y = int(hand_landmarks.landmark[self.THUMB_TIP].y * image.shape[0])

            # get the x and y cordinates of the wrist
            wrist_x = int(hand_landmarks.landmark[self.WRIST].x * image.shape[1])
            wrist_y = int(hand_landmarks.landmark[self.WRIST].y * image.shape[0])

            # get the x and y cordinates of the pinky tip
            pinky_tip_x = int(hand_landmarks.landmark[self.PINKY_TIP].x * image.shape[1])
            pinky_tip_y = int(hand_landmarks.landmark[self.PINKY_TIP].y * image.shape[0])

            # check if the hand is left or right
            if handedness.classification[0].label.lower() == "left":
                left_hand_cordinates = Hand(
                    index_finger_tip=Cordinates(x=index_finger_tip_x, y=index_finger_tip_y),
                    middle_finger_tip=Cordinates(x=middle_finger_tip_x, y=middle_finger_tip_y),
                    thumb_tip=Cordinates(x=thumb_tip_x, y=thumb_tip_y),
                    wrist=Cordinates(x=wrist_x, y=wrist_y),
                    pinky_tip=Cordinates(x=pinky_tip_x, y=pinky_tip_y),
                )
            else:
                right_hand_cordinates = Hand(
                    index_finger_tip=Cordinates(x=index_finger_tip_x, y=index_finger_tip_y),
                    middle_finger_tip=Cordinates(x=middle_finger_tip_x, y=middle_finger_tip_y),
                    thumb_tip=Cordinates(x=thumb_tip_x, y=thumb_tip_y),
                    wrist=Cordinates(x=wrist_x, y=wrist_y),
                    pinky_tip=Cordinates(x=pinky_tip_x, y=pinky_tip_y),
                )

        # return the cordinates
        return HandCoordinates(
            left_hand=left_hand_cordinates, right_hand=right_hand_cordinates
        )

    def is_palm_visible(self, coordinates: HandCoordinates) -> bool:
        """
        This method is used to check if the palm is visible.

        Args:
            coordinates: The coordinates of the index, middle and thumb tips.

        Returns:
            bool: True if the palm is visible, False otherwise.
        """

        # check if the coordinates are not none
        if not coordinates:
            return False

        # check if the left hand's palm is visible
        if coordinates.left_hand and coordinates.left_hand.pinky_tip.x < coordinates.left_hand.thumb_tip.x:
            return True

        # check if the right hand's palm is visible
        if coordinates.right_hand and coordinates.right_hand.pinky_tip.x > coordinates.right_hand.thumb_tip.x:
            return True

        return False