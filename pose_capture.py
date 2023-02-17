import cv2
import mediapipe as mp
import numpy as np
import time

# initialize the MediaPipe pose model
mp_pose = mp.solutions.pose.Pose()

# initialize the video capture
cap = cv2.VideoCapture(0)

# create a blank image to draw the stick figure on
stick_figure = None

# flag to indicate if the button is currently being pressed
button_pressed = False

# callback function for the button
def button_callback(event, x, y, flags, param):
    global button_pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        button_pressed = True

# create a window with the button
cv2.namedWindow('Stick Figure')
cv2.setMouseCallback('Stick Figure', button_callback)

# continuously process the webcam feed
while True:
    # read a frame from the video capture
    ret, frame = cap.read()

    # convert the frame to RGB format
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect the pose landmarks in the frame
    pose = mp_pose.process(image=rgb)
    landmarks = pose.pose_landmarks

    # if landmarks are detected, draw the stick figure
    if landmarks is not None:
        # define the connections between the key points
        connections = [(12, 11), (11, 23), (24, 23), (24, 12), (24, 26), (26, 28), (23, 25), (25, 27), (28, 32), (32, 30), (28, 30), (27, 31), (29, 31), (27, 29), (14, 12), (14, 16), (11, 13), (13, 15), (8, 6), (3, 7), (10, 9), (6, 5), (5, 4), (4, 0), (3, 2), (2, 1), (1, 0), (16, 18), (18, 20), (20, 16), (16, 22), (15, 21), (15, 19), (19, 17), (17, 15), (12, 23), (11, 24)]

        # draw lines between the key points to form the stick figure
        stick_figure = np.zeros_like(frame)
        for connection in connections:
            x1 = int(landmarks.landmark[connection[0]].x * frame.shape[1])
            y1 = int(landmarks.landmark[connection[0]].y * frame.shape[0])
            x2 = int(landmarks.landmark[connection[1]].x * frame.shape[1])
            y2 = int(landmarks.landmark[connection[1]].y * frame.shape[0])
            cv2.line(stick_figure, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # if the button is pressed, save the stick figure to a file after 3 seconds
    if button_pressed:
        # display the countdown timer
        for i in range(3, 0, -1):
            cv2.putText(frame, str(i), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Stick Figure', frame)
            cv2.waitKey(1000)
        
        # write the lines of the stick figure to a
