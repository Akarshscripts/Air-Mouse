"""
This is the main module for the application.
"""

# 1st party imports
import json

# 3rd party imports
import cv2

# local imports
from config import SHOW_IMAGE
from detector.detector import Detector
from camera_handler.camera import CameraHandler
from mouse_handler.mouse_handler import MouseHandler

# create instances
camera_handler = CameraHandler()
detector = Detector()
mouse_handler = MouseHandler()

# run the camera
while camera_handler.cap.isOpened():

    # get the frame and check if it is successful
    success, orignal_image = camera_handler.get_frame()

    # if the frame is not successful, continue
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # preprocess the image
    processed_image = camera_handler.preprocess_image_for_hands(orignal_image)

    # Process the image and detect hands
    results = detector.detect_hands(processed_image)

    # get the cordinates of the index, middle and thumb tips
    coordinates = detector.get_cordinates(results, orignal_image)

    # show the image if in debug mode
    if SHOW_IMAGE:
        # Draw hand landmarks
        drawn_image = camera_handler.draw_hand_landmarks(coordinates, orignal_image)

        # show the image
        camera_handler.show_image(drawn_image)

    # check if palm is visible
    palm_is_visible = detector.is_palm_visible(coordinates)

    # check if palm is visible
    if palm_is_visible:

        # perform actions based on the landmarks
        mouse_handler.handle_mouse_actions(coordinates)

    # Break on 'q' key
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

camera_handler.cap.release()
cv2.destroyAllWindows()

# Complete