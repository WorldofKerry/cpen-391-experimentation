import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()

    frame = cv2.resize(frame, (320, 240))
    
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    green = cv2.inRange(frame_hsv, (58, 71, 0), (100, 191, 255))
    green_list = cv2.findNonZero(green)
    green_list = green_list.reshape(-1, 2)
    green_list = np.float32(green_list)
    # print(green_list.shape)
    
    # convert green to 3 channels
    green = cv2.cvtColor(green, cv2.COLOR_GRAY2BGR)

    if green_list is not None:
        # run dbscan on green_list
        db = DBSCAN(eps=4, min_samples=30).fit(green_list)
        labels = db.labels_
        # print(labels.shape)
        
        # get the largest cluster
        largest_cluster = 0
        largest_cluster_size = 0
        second_largest_cluster = 0
        second_largest_cluster_size = 0
        for i in range(len(labels)):
            if labels[i] == largest_cluster:
                largest_cluster_size += 1
            elif labels[i] == second_largest_cluster:
                second_largest_cluster_size += 1
            elif largest_cluster_size < second_largest_cluster_size:
                largest_cluster = second_largest_cluster
                largest_cluster_size = second_largest_cluster_size
                second_largest_cluster = labels[i]
                second_largest_cluster_size = 1
            else:
                second_largest_cluster = labels[i]
                second_largest_cluster_size = 1

        # get centroid of largest cluster
        centroid = np.mean(green_list[labels == largest_cluster], axis=0)
        second_centroid = np.mean(green_list[labels == second_largest_cluster], axis=0)

        # draw red circle on centroid
        print(largest_cluster_size)
        if largest_cluster_size > 300:
            cv2.circle(green, (int(centroid[0]), int(centroid[1])), 10, (0, 0, 255), -1)

        # draw blue circle on centroid
        # print(second_largest_cluster_size)
        if second_largest_cluster_size > 300:
            cv2.circle(green, (int(second_centroid[0]), int(second_centroid[1])), 10, (255, 0, 0), -1)

    # show binary image
    cv2.imshow('Binary', green)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()