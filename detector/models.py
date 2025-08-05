"""
This module contains the models for the application.
"""

# 1st party imports
from typing import Optional, List
from dataclasses import dataclass

# 3rd party imports
from pydantic import BaseModel
from mediapipe.framework.formats import classification_pb2, landmark_pb2


@dataclass
class HandDetectionResult:
    """
    This class is used to store the results of the hand detection.
    """

    multi_hand_landmarks: Optional[List[landmark_pb2.NormalizedLandmarkList]]
    multi_handedness: Optional[List[classification_pb2.ClassificationList]]
    multi_hand_world_landmarks: Optional[List[landmark_pb2.LandmarkList]]


class Cordinates(BaseModel):
    """
    This class is used to store the cordinates of the landmarks.
    """

    x: int
    y: int


class Hand(BaseModel):
    """
    This class is used to store the hand cordinates.
    """

    index_finger_tip: Cordinates
    middle_finger_tip: Cordinates
    thumb_tip: Cordinates
    wrist: Cordinates
    pinky_tip: Cordinates


class HandCoordinates(BaseModel):
    """
    This class is used to store the cordinates of both hands.
    """

    left_hand: Optional[Hand]
    right_hand: Optional[Hand]
