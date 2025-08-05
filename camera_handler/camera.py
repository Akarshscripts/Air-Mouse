"""
This module contains the camera handler class for the application.
It is used to handle the camera feed and process it.
"""

# 1st party imports
import time

# 3rd party imports
import cv2
import numpy as np

# local imports
from detector.models import HandCoordinates, Hand


class CameraHandler:
    """
    This class is used to handle the camera feed and process it.
    """

    def __init__(self, camera_id: int = 0):
        """
        This method is used to initialize the camera.
        """

        # initialize the camera
        self.cap = cv2.VideoCapture(camera_id)

        # set the time for fps display
        self.fps_time = time.time()

    def get_frame(self) -> tuple[bool, np.ndarray]:
        """
        This method is used to get the frame from the camera.
        """

        # read the image
        success, image = self.cap.read()

        # check if the image is read successfully
        if not success:
            return success, image

        # Flip the image horizontally for natural selfie view
        image = cv2.flip(image, 1)

        return success, image

    def preprocess_image_for_hands(self, image: np.ndarray) -> np.ndarray:
        """
        This method is used to preprocess the image for hands.

        Args:
            image: The image to preprocess.

        Returns:
            The preprocessed image.
        """

        # Convert BGR to RGB (MediaPipe uses RGB)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return image

    def show_image(self, image: np.ndarray, display_fps: bool = True) -> None:
        """
        This method is used to show the image.

        Args:
            image: The image to show.
            display_fps: Whether to display the fps or not.
        """

        # update the fps
        fps = 1.0 / (time.time() - self.fps_time)

        # display the fps
        if display_fps:
            cv2.putText(
                image,
                f"FPS: {int(fps)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (122, 218, 165),
                2,
            )

        # Show the image
        cv2.imshow("MediaPipe Hands", image)

        # update the fps time
        self.fps_time = time.time()

    def __draw_landmarks(
        self,
        hand_cords: Hand,
        image: np.ndarray,
        color_dot: tuple = (255, 0, 0),
        color_outline: tuple = (255, 0, 0),
    ) -> np.ndarray:
        """
        This method is used to draw the hand landmarks on the image.

        Args:
            hand_cords: The hand landmarks to draw.
            image: The image to draw the hand landmarks on.
            color: The color to be used.

        Returns:
            The image with hand landmarks drawn.
        """

        # draw on the index finger
        cv2.circle(
            image,
            (hand_cords.index_finger_tip.x, hand_cords.index_finger_tip.y),
            3,
            color_dot,
            -1,
            cv2.LINE_8,
        )
        cv2.circle(
            image,
            (hand_cords.index_finger_tip.x, hand_cords.index_finger_tip.y),
            25,
            color_outline,
            1,
            cv2.LINE_AA,
        )

        # draw on the middle finger
        cv2.circle(
            image,
            (hand_cords.middle_finger_tip.x, hand_cords.middle_finger_tip.y),
            3,
            color_dot,
            -1,
            cv2.LINE_8,
        )
        cv2.circle(
            image,
            (hand_cords.middle_finger_tip.x, hand_cords.middle_finger_tip.y),
            25,
            color_outline,
            1,
            cv2.LINE_AA,
        )

        # draw on the thumb finger
        cv2.circle(
            image,
            (hand_cords.thumb_tip.x, hand_cords.thumb_tip.y),
            3,
            color_dot,
            -1,
            cv2.LINE_8,
        )
        cv2.circle(
            image,
            (hand_cords.thumb_tip.x, hand_cords.thumb_tip.y),
            25,
            color_outline,
            1,
            cv2.LINE_AA,
        )

        return image

    def draw_hand_landmarks(
        self, coordinates: HandCoordinates, image: np.ndarray
    ) -> np.ndarray:
        """
        This method is used to draw the hand landmarks on the image.

        Args:
            coordinates: The coordinates of the index, middle and thumb tips.
            image: The image to draw the hand landmarks on.

        Returns:
            The image with hand landmarks drawn.
        """

        # check if the coordinates are not none
        if not coordinates or (
            not coordinates.left_hand and not coordinates.right_hand
        ):
            return image

        # circle color
        small_circle_color = (228, 240, 241)
        big_circle_color = (106, 209, 254)

        # draw on left hand
        if coordinates.left_hand:
            self.__draw_landmarks(
                coordinates.left_hand, image, small_circle_color, big_circle_color
            )

        # draw on right hand
        if coordinates.right_hand:
            self.__draw_landmarks(
                coordinates.right_hand, image, small_circle_color, big_circle_color
            )

        return image
