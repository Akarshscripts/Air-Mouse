"""
This module holds the logic for the mouse handler used in this project
"""

# 1st party imports
import time
import math
from typing import Optional
from collections import deque

# 3rd party imports
import ctypes
import numpy as np

# local imports
from mouse_handler.helper import Smoother
from detector.models import HandCoordinates, Hand


class POINT(ctypes.Structure):
    """
    This class is used to define the POINT structure for GetCursorPos.
    """

    _fields_ = [("x", ctypes.wintypes.LONG), ("y", ctypes.wintypes.LONG)]


class MouseHandler:
    """
    This class is used to handle the mouse events.
    """

    def __init__(self, mouse_sensi: float = 4.0):
        """
        This method is used to initialize the mouse handler.
        """

        # set the mouse senstivity
        self.mouse_sensi = mouse_sensi

        # set the mouse offset
        self.mouse_offset = None

        # set the smoother instance
        self.movement_smoother = Smoother()
        self.right_click_smoother = Smoother(max_len=5)
        self.left_click_smoother = Smoother(max_len=5)

        # set the last click time
        self.last_left_click = time.time()
        self.last_right_click = time.time()

    def left_click(self) -> None:
        """
        This method is used to perform a right click.
        """

        # check if the last click was atleast 2 seconds ago
        if time.time() - self.last_left_click < 1:
            return

        # perform the right click
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
        time.sleep(0.1)
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)

        # set the last click time
        self.last_left_click = time.time()

    def right_click(self) -> None:
        """
        This method is used to perform a left click.
        """

        # check if the last click was atleast 2 seconds ago
        if time.time() - self.last_right_click < 1:
            return

        # perform the left click
        ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
        time.sleep(0.1)
        ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)

        # set the last click time
        self.last_right_click = time.time()

    def move_mouse_to(self, x: int, y: int) -> None:
        """
        This method is used to move the mouse to the a particular position.

        Args:
            x: The x coordinate of the position.
            y: The y coordinate of the position.
        """

        # smooth the mouse position
        x, y = self.movement_smoother.smooth(x, y)

        # move the mouse to the position of the index finger tip
        ctypes.windll.user32.SetCursorPos(x, y)

    def get_mouse_position(self) -> tuple[int, int]:
        """
        This method is used to get the mouse position.

        Returns:
            tuple[int, int]: The mouse position.
        """
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    def handle_mouse_actions(
        self, coordinates: Optional[HandCoordinates] = None
    ) -> None:
        """
        This method is used to handle the mouse actions based on the coordinates.

        Args:
            coordinates: The coordinates of the index, middle and thumb tips of both hands.
        """

        # check if the coordinates are not none
        if not coordinates:
            return

        # move the mouse to the position of the index finger tip
        move_gesture_cords, move_gesture_shown = self.move_gesture_shown(coordinates)
        if move_gesture_shown:

            # set the offset if not already calculated
            if not self.mouse_offset:

                # get current mouse position
                current_mouse_position = self.get_mouse_position()

                # calculate the offset
                self.mouse_offset = (
                    current_mouse_position[0] - move_gesture_cords[0],
                    current_mouse_position[1] - move_gesture_cords[1],
                )

            # calculate the new mouse position
            new_mouse_position = (
                move_gesture_cords[0] + self.mouse_offset[0],
                move_gesture_cords[1] + self.mouse_offset[1],
            )

            # move the mouse
            self.move_mouse_to(int(new_mouse_position[0]), int(new_mouse_position[1]))
        else:
            self.mouse_offset = None

        # check if a right click is detected
        if self.is_right_click(coordinates):
            self.right_click()

        # check if a left click is detected
        if self.is_left_click(coordinates):
            self.left_click()

        return

    def move_gesture_shown(
        self, coordinates: HandCoordinates
    ) -> tuple[list[int], bool]:
        """
        This method is used to check if the mouse move action is detected.

        Args:
            coordinates: The coordinates of the index, middle and thumb tips of both hands.

        Returns:
            tuple[list[int], bool]: The coordinates of the mouse and a boolean value indicating if the mouse move action is detected.
        """

        # prefer right hand if available
        calculable_hand = (
            coordinates.right_hand if coordinates.right_hand else coordinates.left_hand
        )

        # if right hand is available find the angle
        angle = self.__get_angle(calculable_hand)

        # check if the angle is within the range
        if angle > 8:
            return [0, 0], False

        # return the point after adjusting for senstivity
        return [
            int(calculable_hand.index_finger_tip.x * self.mouse_sensi),
            int(calculable_hand.index_finger_tip.y * self.mouse_sensi),
        ], True

    def __get_angle(self, hand: Hand) -> float:
        """
        This method is used to get the angle between the wrist - the index and the middle finger.

        Args:
            hand: The hand coordinates.

        Returns:
            float: The angle between the wrist - the index and the middle finger.
        """

        # create numpy arrays
        wrist = np.array([hand.wrist.x, hand.wrist.y])
        index_tip = np.array([hand.index_finger_tip.x, hand.index_finger_tip.y])
        middle_tip = np.array([hand.middle_finger_tip.x, hand.middle_finger_tip.y])

        # Calculate the dot product
        dot_product = np.dot(index_tip - wrist, middle_tip - wrist)

        # Calculate the magnitudes of the vectors
        mag_v1 = np.linalg.norm(index_tip - wrist)
        mag_v2 = np.linalg.norm(middle_tip - wrist)

        if mag_v1 == 0 or mag_v2 == 0:
            return 0

        # calculate the cos of the angle
        cos_theta = dot_product / (mag_v1 * mag_v2)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)

        # calculate the angle in degrees
        return math.degrees(math.acos(cos_theta))

    def is_left_click(self, coordinates: HandCoordinates, threshold: int = 25) -> bool:
        """
        This method is used to check if a left click is detected.

        Args:
            coordinates: The coordinates of the index, middle and thumb tips of both hands.

        Returns:
            bool: True if a right click is detected, False otherwise.
        """

        # prefer right hand if available
        calculable_hand = (
            coordinates.right_hand if coordinates.right_hand else coordinates.left_hand
        )

        # if the index finger tip is close to the thumb tip
        distance = math.hypot(
            calculable_hand.index_finger_tip.x - calculable_hand.thumb_tip.x,
            calculable_hand.index_finger_tip.y - calculable_hand.thumb_tip.y,
        )

        # check if the distance is within the range
        if distance < threshold:
            return True

        return False

    def is_right_click(self, coordinates: HandCoordinates, threshold: int = 25) -> bool:
        """
        This method is used to check if a right click is detected.

        Args:
            coordinates: The coordinates of the index, middle and thumb tips of both hands.

        Returns:
            bool: True if a right click is detected, False otherwise.
        """

        # prefer right hand if available
        calculable_hand = (
            coordinates.right_hand if coordinates.right_hand else coordinates.left_hand
        )

        # if the index finger tip is close to the thumb tip
        distance = math.hypot(
            calculable_hand.middle_finger_tip.x - calculable_hand.thumb_tip.x,
            calculable_hand.middle_finger_tip.y - calculable_hand.thumb_tip.y,
        )

        # check if the distance is within the range
        if distance < threshold:
            return True

        return False
