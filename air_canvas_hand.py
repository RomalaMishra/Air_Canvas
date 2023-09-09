# Import necessary libraries
import cv2
import numpy as np
import mediapipe as mp
import time
import os
import HandTrack as htp

# Set brush and eraser thickness for drawing
brushthickness = 25
eraserthickness = 100

# Initialize drawing coordinates
xp, yp = 0, 0

# Create a blank canvas to draw on
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

# Load overlay images for the drawing header
folderPath = "Header"
myList = os.listdir(folderPath)
overlaylist = []
for inPath in myList:
    image = cv2.imread(f'{folderPath}/{inPath}')
    overlaylist.append(image)
header = overlaylist[0]

# Set initial drawing color
drawColor = (255, 0, 255)

# Initialize the webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize the hand detector
detector = htp.handDetector(detectionCon=0.85)

# Main loop for real-time hand detection and drawing
while True:
    success, img = cap.read()
    if not success:
        break

    # Flip the image horizontally for a mirrored view
    img = cv2.flip(img, 1)

    # Detect hands in the frame
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        # Check finger positions for gesture recognition
        fingers = detector.fingersUp()

        if fingers[1] and fingers[2]:
            # Selection mode: Change color based on the selected area
            xp, yp = 0, 0
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlaylist[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlaylist[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlaylist[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlaylist[3]
                    drawColor = (0, 0, 0)

        if fingers[1] and not fingers[2]:
            # Drawing mode: Draw lines on the canvas
            cv2.circle(img, (x1, y1), 25, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Determine whether to draw or erase
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserthickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserthickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushthickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushthickness)

            xp, yp = x1, y1

    # Apply canvas and header to the displayed image
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:125, 0:1280] = header

    # Display the canvas and image
    cv2.imshow("Canvas", imgCanvas)
    cv2.imshow("Image", img)

    # Wait for a key press (1ms) and exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up and close the OpenCV windows
cv2.destroyAllWindows()
