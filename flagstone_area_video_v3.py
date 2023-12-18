# Christian Amundsen
# Detecting stones from video or live feed

import cv2
import numpy as np
import csv
import datetime 
import math

#######################################################################################
### Functions ###

def isRectangular(cnt, threshold_degrees=5):
    if len(cnt) != 4:
        return False

    angles = []
    for i in range(4):
        # Calculate the angle between consecutive vertices
        pt1 = cnt[i][0]
        pt2 = cnt[(i + 1) % 4][0]
        pt3 = cnt[(i + 2) % 4][0]

        vector1 = (pt1[0] - pt2[0], pt1[1] - pt2[1])
        vector2 = (pt3[0] - pt2[0], pt3[1] - pt2[1])

        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
        magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

        angle = math.acos(dot_product / (magnitude1 * magnitude2)) * (180 / math.pi)
        angles.append(angle)

    for angle in angles:
        if abs(90 - angle) > threshold_degrees:
            return False

    return True

def timeFromFrame(frame, oldTime):
    time_delta = frame//30
    newTime = oldTime + datetime.timedelta(seconds=time_delta)

    return newTime

#######################################################################################

# Input
video = 1

if   video == 1: video_path, video_start = "Minera1-video.mp4",  datetime.datetime.strptime("10:02:30", "%H:%M:%S")
elif video == 2: video_path, video_start = "Minera2-video.mp4",  datetime.datetime.strptime("12:51:05", "%H:%M:%S")
elif video == 3: video_path, video_start = "Minera3-video.mp4",  datetime.datetime.strptime("07:01:45", "%H:%M:%S")
elif video == 4: video_path, video_start = "Minera4-video.mp4",  datetime.datetime.strptime("10:04:45", "%H:%M:%S")
elif video == 5: video_path, video_start = "Kalibrering480.mp4", 0
elif video == 6: video_path, video_start = "Minera_testvideo.mp4", datetime.datetime.strptime("10:04:45", "%H:%M:%S")

csv_file = 'test.csv' 

# Tolerances for removing bad readings
min_stone_area = 110000  # Adjust this value as needed
edge_margin = 2  # Adjust this value as needed

# Tolerances for filtering out multiple readings of same stone
area_tolerance = 10000
side_lenght_tolerance = 5
time_tolerance = 2
time_tolerance_long = 10

# Scaling
#scaleFactor = 10/7   # For 1080p
#scaleFactor = 15/7   # For 720p
scaleFactor = 30/7   # For 480p

# Cropping
xMin = 100
xMax = 500
yMin = 0
yMax = -1

# Image manupilation
contrast = 1   # 1 is no change
brightness = 1 # 1 is no change 

#######################################################################################

# Initialize video capture from a file
cap = cv2.VideoCapture(video_path)
frameNum = 0

# Initialize CSV file for logging data
csv_header = ['Timestamp', 'Stone_Index', 'Area', 'Corners', 'Shape', 'Side1_Length', 'Side2_Length']
with open(csv_file, 'w', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(csv_header)

stone_index = 0  # Index to track the number of stones detected

# Define the fixed text position
text_position = (20, 40)  # Adjust the (x, y) coordinates as needed
text_line_spacing = 20  # Adjust the spacing between lines

# Initialize variables to store the characteristics of the last logged stone
last_area = 0.0
last_shape = "N/A"
last_side1_length = 0.0
last_side2_length = 0.0

# Initialize variables to store the timestamp of the last logged frame
last_timestamp = datetime.datetime.now()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = frame[yMin:yMax, xMin:xMax]

    time = timeFromFrame(frameNum, video_start)

    # Initialize area, shape, and side lengths to default values
    area = 0.0
    shape = "N/A"
    side1_length = 0.0
    side2_length = 0.0

    # Convert frame to greyscale
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(frame, 0, 100)
    grey = cv2.convertScaleAbs(grey, alpha=contrast, beta=brightness)
    

    # Threshold the greyscale image to separate the stones from the background
    ret, thresh = cv2.threshold(grey, 100, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    #contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    stones_contours = []

    for contour in contours:
        # Calculate area of the contour
        area = cv2.contourArea(contour) * scaleFactor**2

        # Check if the stone is above the minimum area threshold
        if area >= min_stone_area:
            # Approximate the contour to find the number of corners
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            num_corners = len(approx)

            stones_contours.append(contour)

            # Check if the stone is far enough from the image edges
            x, y, w, h = cv2.boundingRect(contour)
            if (
                x >= edge_margin
                and y >= edge_margin
                and x + w <= frame.shape[1] - edge_margin
                and y + h <= frame.shape[0] - edge_margin
            ):
                if isRectangular(approx):
                    # Classify the shape as "rectangular"
                    shape = "rectangular"

                    # Calculate side lengths of the rectangular stone
                    side1_length = round(np.linalg.norm(approx[0] - approx[1])) * scaleFactor
                    side2_length = round(np.linalg.norm(approx[1] - approx[2])) * scaleFactor

                else:
                    # Classify the shape as "irregular"
                    shape = "irregular"

                # Get the timestamp of the current frame
                current_timestamp = datetime.datetime.now()
                print(current_timestamp)

                if num_corners > 2:

                    # Check if the current frame is significantly different from the last logged frame
                    if (
                        abs(area - last_area) > area_tolerance
                        #or shape != last_shape
                        or abs(side1_length - last_side1_length) > side_lenght_tolerance
                        or abs(side2_length - last_side2_length) > side_lenght_tolerance
                        or (int(current_timestamp.timestamp()) - int(last_timestamp.timestamp())) > time_tolerance_long
                    ):
                        if ((int(current_timestamp.timestamp()) - int(last_timestamp.timestamp())) > time_tolerance):
                            
                            # Log data to CSV file
                            with open(csv_file, 'a', newline='') as f:
                                csv_writer = csv.writer(f)
                                csv_writer.writerow([time.time(), stone_index, round(area), num_corners, shape, round(side1_length), round(side2_length)])

                            stone_index += 1

                            # Update the variables for the last logged stone and frame
                            last_area = area
                            last_shape = shape
                            last_side1_length = side1_length
                            last_side2_length = side2_length
                            last_timestamp = current_timestamp


    # Build the text for overlay with line breaks

    text_lines = [
        f"Area: {last_area:.2f}"
        ,f"Shape: {last_shape}"
        ,f"Side1 Length: {last_side1_length:.2f}"
        ,f"Side2 Length: {last_side2_length:.2f}"
        ,f"Time: {time.time()}"
    ]

    # Draw the contour on the frame
    #cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    #cv2.drawContours(frame, stones_contours, -1, (0, 255, 0), 2)
    #cv2.drawContours(grey, contours, -1, (0, 255, 0), 2)
    #cv2.drawContours(grey, stones_contours, -1, (0, 255, 0), 2)
    #cv2.drawContours(thresh, stones_contours, -1, (0, 255, 0), 2)

    # Draw the fixed text overlay on the frame with separate lines
    #for i, line in enumerate(text_lines):
    #    y_offset = text_position[1] + i * text_line_spacing
    #    cv2.putText(frame, line, (text_position[0], y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with contour overlay and fixed text overlay
    #cv2.imshow('Frame', frame)
    cv2.imshow('FrameGrey', canny)
    cv2.imshow('Frametresh', thresh)

    frameNum += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()