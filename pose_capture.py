import cv2
import mediapipe as mp
import numpy as np

# initialize the MediaPipe pose model
mp_pose = mp.solutions.pose.Pose()

# initialize the video capture
cap = cv2.VideoCapture(0)

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
        # create a blank image to draw the stick figure on
        stick_figure = np.zeros_like(frame)

        # define the connections between the key points
        connections = [(12, 11), (11, 23), (24, 23), (24, 12), (24, 26), (26, 28), (23, 25), (25, 27), (28, 32), (32, 30), (28, 30), (27, 31), (29, 31), (27, 29), (14, 12), (14, 16), (11, 13), (13, 15), (8, 6), (3, 7), (10, 9), (6, 5), (5, 4), (4, 0), (3, 2), (2, 1), (1, 0), (16, 18), (18, 20), (20, 16), (16, 22), (15, 21), (15, 19), (19, 17), (17, 15), (12, 23), (11, 24)]

        # draw lines between the key points to form the stick figure
        for connection in connections:
            x1 = int(landmarks.landmark[connection[0]].x * frame.shape[1])
            y1 = int(landmarks.landmark[connection[0]].y * frame.shape[0])
            x2 = int(landmarks.landmark[connection[1]].x * frame.shape[1])
            y2 = int(landmarks.landmark[connection[1]].y * frame.shape[0])
            cv2.line(stick_figure, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # blend the stick figure with the original frame using an alpha channel
        alpha = 0.5
        blended = cv2.addWeighted(frame, alpha, stick_figure, 1 - alpha, 0)

        # display the blended image in a window
        cv2.imshow('Stick Figure', blended)

    # check if the user pressed the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the resources
cap.release()
cv2.destroyAllWindows()
