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
    
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    green = cv2.inRange(frame_hsv, (58, 71, 0), (100, 191, 255))
    green_list = cv2.findNonZero(green)
    green_list = green_list.reshape(-1, 2)
    green_list = np.float32(green_list)
    print(green_list.shape)
    
    # convert green to 3 channels
    green = cv2.cvtColor(green, cv2.COLOR_GRAY2BGR)

    if green_list is not None:
        # run dbscan on green_list
        db = DBSCAN(eps=5, min_samples=60).fit(green_list)
        labels = db.labels_
        # print(labels.shape)
        
        # get the largest cluster
        largest_cluster = 0
        largest_cluster_size = 0
        for i in range(labels.max()):
            cluster_size = np.count_nonzero(labels == i)
            if cluster_size > largest_cluster_size:
                largest_cluster_size = cluster_size
                largest_cluster = i

        # get the centroid of the largest cluster
        largest_cluster_list = green_list[labels == largest_cluster]
        centroid = np.mean(largest_cluster_list, axis=0)
        # print(centroid)

        # draw red circle on centroid
        print(largest_cluster_size)
        if largest_cluster_size > 700:
            cv2.circle(frame, (int(centroid[0]), int(centroid[1])), 10, (0, 0, 255), -1)

    # show binary image
    cv2.imshow('Binary', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()