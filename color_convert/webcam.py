import cv2

# Initialize the YCbCr and HSV threshold values
cb_min = 0
cb_max = 255
cr_min = 0
cr_max = 255
hue_min = 0
hue_max = 255
sat_min = 0
sat_max = 255
val_min = 0
val_max = 255

# Colors for Green Brain Object
cb_min = 121
cb_max = 130
cr_min = 97
cr_max = 120

# Define a callback function for the trackbars
def update_thresholds(*args):
    global cb_min, cb_max, cr_min, cr_max, hue_min, hue_max, sat_min, sat_max, val_min, val_max
    cb_min = cv2.getTrackbarPos('Cb_min', 'Filtered Webcam')
    cb_max = cv2.getTrackbarPos('Cb_max', 'Filtered Webcam')
    cr_min = cv2.getTrackbarPos('Cr_min', 'Filtered Webcam')
    cr_max = cv2.getTrackbarPos('Cr_max', 'Filtered Webcam')
    hue_min = cv2.getTrackbarPos('Hue_min', 'Filtered Webcam')
    hue_max = cv2.getTrackbarPos('Hue_max', 'Filtered Webcam')
    sat_min = cv2.getTrackbarPos('Sat_min', 'Filtered Webcam')
    sat_max = cv2.getTrackbarPos('Sat_max', 'Filtered Webcam')
    val_min = cv2.getTrackbarPos('Val_min', 'Filtered Webcam')
    val_max = cv2.getTrackbarPos('Val_max', 'Filtered Webcam')

# Create a window for the trackbars
cv2.namedWindow('Filtered Webcam')

# Create trackbars for the YCbCr and HSV thresholds
cv2.createTrackbar('Cb_min', 'Filtered Webcam', cb_min, 255, update_thresholds)
cv2.createTrackbar('Cb_max', 'Filtered Webcam', cb_max, 255, update_thresholds)
cv2.createTrackbar('Cr_min', 'Filtered Webcam', cr_min, 255, update_thresholds)
cv2.createTrackbar('Cr_max', 'Filtered Webcam', cr_max, 255, update_thresholds)
# cv2.createTrackbar('Hue_min', 'Filtered Webcam', hue_min, 180, update_thresholds)
# cv2.createTrackbar('Hue_max', 'Filtered Webcam', hue_max, 180, update_thresholds)
# cv2.createTrackbar('Sat_min', 'Filtered Webcam', sat_min, 255, update_thresholds)
# cv2.createTrackbar('Sat_max', 'Filtered Webcam', sat_max, 255, update_thresholds)
# cv2.createTrackbar('Val_min', 'Filtered Webcam', val_min, 255, update_thresholds)
# cv2.createTrackbar('Val_max', 'Filtered Webcam', val_max, 255, update_thresholds)

# Start capturing the default camera feed
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Convert the frame from BGR color space to YCbCr color space
    ycbcr = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    
    # Apply the YCbCr filter based on the current threshold values
    ycbcr_mask = cv2.inRange(ycbcr, (0, cr_min, cb_min), (255, cr_max, cb_max))
    
    # Convert the frame from BGR color space to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Apply the HSV filter based on the current threshold values
    hsv_mask = cv2.inRange(hsv, (hue_min, sat_min, val_min), (hue_max, sat_max, val_max))

    # Combine the YCbCr and HSV masks
    mask = cv2.bitwise_and(ycbcr_mask, hsv_mask)

    # Apply the mask to the frame
    filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the filtered frame
    cv2.imshow('Filtered Webcam', filtered_frame)

    # Check if the user pressed the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()


