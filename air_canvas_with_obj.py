import numpy as np
import cv2
from collections import deque

def setValues(x):
    pass

cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255, setValues)

class AirCanvas():

    def __init__(self):

        # initialising the colour points as deque
        self.bpoints = [deque(maxlen=1024)]
        self.gpoints = [deque(maxlen=1024)]
        self.rpoints = [deque(maxlen=1024)]
        self.ypoints = [deque(maxlen=1024)]

        # initialising the required variables
        self.blue_index = 0
        self.green_index = 0
        self.red_index = 0
        self.yellow_index = 0

        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        self.colorIndex = 0

        # calling this function to establish the paint window
        self.Paintwindow()

        # defining kernel size
        self.kernel = np.ones((5,5),np.uint8)

        self.cap = cv2.VideoCapture(0)

        while (self.cap.isOpened()): 

            ret, frame = self.cap.read()
            self.run(frame)  
        
        self.cap.release()
        cv2.destroyAllWindows()   

    def Paintwindow(self):
         
        # defining the paintwindow
        self.paintWindow = np.zeros((471,636,3)) + 255
        self.paintWindow = cv2.rectangle(self.paintWindow, (40,1), (140,65), (0,0,0), 2)
        self.paintWindow = cv2.rectangle(self.paintWindow, (160,1), (255,65), self.colors[0], -1)
        self.paintWindow = cv2.rectangle(self.paintWindow, (275,1), (370,65), self.colors[1], -1)
        self.paintWindow = cv2.rectangle(self.paintWindow, (390,1), (485,65), self.colors[2], -1)
        self.paintWindow = cv2.rectangle(self.paintWindow, (505,1), (600,65), self.colors[3], -1)

        cv2.putText(self.paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
        cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

    def draw(self,frame):

        # Adding the colour buttons to the live frame for colour access
        frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
        frame = cv2.rectangle(frame, (160,1), (255,65), self.colors[0], -1)
        frame = cv2.rectangle(frame, (275,1), (370,65), self.colors[1], -1)
        frame = cv2.rectangle(frame, (390,1), (485,65), self.colors[2], -1)
        frame = cv2.rectangle(frame, (505,1), (600,65), self.colors[3], -1)

        cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)            

    def paint(self,frame):

        # Draw lines of all the colors on the canvas and frame 
        points = [self.bpoints, self.gpoints, self.rpoints, self.ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], self.colors[i], 2)
                    cv2.line(self.paintWindow, points[i][j][k - 1], points[i][j][k], self.colors[i], 2)
     
    def run(self, frame):

        # flipping the frame
        frame = cv2.flip(frame, 1)
        
        # converting the frame from BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # getting the trackbar
        u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
        u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
        u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
        l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
        l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
        l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")

        Upper_hsv = np.array([u_hue,u_saturation,u_value])
        Lower_hsv = np.array([l_hue,l_saturation,l_value])

        self.draw(frame)

        # Identifying the pointer by making its mask
        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
        Mask = cv2.erode(Mask, self.kernel, iterations=1)
        Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, self.kernel)
        Mask = cv2.dilate(Mask, self.kernel, iterations=1)

        # Find contours for the pointer after idetifying it
        cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE)
        center = None

         # Ifthe contours are formed
        if len(cnts) > 0:

            # sorting the contours to find biggest contour
            cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

            # Get the radius of the enclosing circle around the found contour
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)

            # Draw the circle around the contour
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

            # Calculating the center of the detected contour
            M = cv2.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            # Now checking if the user wants to click on any button above the screen 
            if center[1] <= 65:

                if 40 <= center[0] <= 140: # Clear Button

                    self.blue_index = 0
                    self.green_index = 0
                    self.red_index = 0
                    self.yellow_index = 0

                    self.paintWindow[67:,:,:] = 255

                elif 160 <= center[0] <= 255:
                        self.colorIndex = 0 # Blue
                elif 275 <= center[0] <= 370:
                        self.colorIndex = 1 # Green
                elif 390 <= center[0] <= 485:
                        self.colorIndex = 2 # Red
                elif 505 <= center[0] <= 600:
                        self.colorIndex = 3 # Yellow
            else :

                if self.colorIndex == 0:
                    self.bpoints[self.blue_index].appendleft(center)
                elif self.colorIndex == 1:
                    self.gpoints[self.green_index].appendleft(center)
                elif self.colorIndex == 2:
                    self.rpoints[self.red_index].appendleft(center)
                elif self.colorIndex == 3:
                    self.ypoints[self.yellow_index].appendleft(center)

        # Append the next deques when nothing is detected to avoid messing up
        else:
            self.bpoints.append(deque(maxlen=512))
            self.blue_index += 1

            self.gpoints.append(deque(maxlen=512))
            self.green_index += 1

            self.rpoints.append(deque(maxlen=512))
            self.red_index += 1

            self.ypoints.append(deque(maxlen=512))
            self.yellow_index += 1

        self.paint(frame)    

        # Show all the windows
        frame = cv2.resize(frame, (1250, 1250), interpolation=cv2.INTER_AREA)
        self.paintWindow = cv2.resize(self.paintWindow, (1250, 1250), interpolation=cv2.INTER_AREA)
        cv2.imshow("Tracking", frame)
        cv2.imshow("Paint", self.paintWindow)
   
        cv2.waitKey(1)

if __name__ == '__main__':
    AirCanvas()
