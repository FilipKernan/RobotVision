# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import numpy as np
import cv2
import logging
import math
import os
import time
from numpy import log
logging.basicConfig(level=logging.DEBUG)


LOWER_GREEN = np.array([45, 0, 180])

UPPER_GREEN = np.array([80, 256, 256])


FRAME_CX = 1280/2
FRAME_CY = 780/2
# Calibration box dimensions
CAL_AREA = 1600
CAL_SIZE = int(math.sqrt(CAL_AREA))
CAL_UP = FRAME_CY + (CAL_SIZE / 2)
CAL_LO = FRAME_CY - (CAL_SIZE / 2)
CAL_R = FRAME_CX - (CAL_SIZE / 2)
CAL_L = FRAME_CX + (CAL_SIZE / 2)
CAL_UL = (CAL_L, CAL_UP)
CAL_LR = (CAL_R, CAL_LO)





def polygon(c):
    """Remove concavities from a contour and turn it into a polygon."""
    hull = cv2.convexHull(c)
    epsilon = 0.025 * cv2.arcLength(hull, True)
    goal = cv2.approxPolyDP(hull, epsilon, True)
    return goal 

def calibration_box(img):
    """Return HSV color in the calibration box."""
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.rectangle(img, CAL_UL, CAL_LR, (0, 255, 0), thickness=1)
    roi = img[CAL_LO:CAL_UP, CAL_R:CAL_L]
    average_color_per_row = np.average(roi, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    average_color = np.uint8([[average_color]])
    
    return average_color

def findDistance(area):
    #puts the area through the function to get distace
    area = area - 1251.1
    dis = math.pow(area, -0.27052)
    dis = dis * 545.16
    dis = dis - 18.387
    return dis
    

def findTargets(contours):
    for i in range(0,2):
        if (i < 1):
            largestContour = max(contours, key = cv2.contourArea)
            secondLargestContour = min(contours, key = cv2.contourArea)
        for c in contours:
            if(cv2.contourArea(c) != cv2.contourArea(largestContour)):
                if(cv2.contourArea(c) > cv2.contourArea(secondLargestContour)):
                    secondLargestContour = c
    return largestContour, secondLargestContour



def capture():
    cap = cv2.VideoCapture(0)
    time.sleep(2)

    while(True):
        # Capture frame-by-frame
        _, frame = cap.read()
        #operations on frame
        frame = cv2.GaussianBlur(frame, (11,11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
        res = cv2.bitwise_and(frame,frame, mask = mask) 
        _, cnts, _= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        try:
            if len(cnts) > 0:
                # finds the two largest areas
                largestArea,secondLargestArea = findTargets(cnts)
                #converts the areas into a polygon 
                nearStrip = polygon(largestArea)
                farStrip = polygon(secondLargestArea)    
                # Gets the average area and then finds the distance using that  
                area = 0
                for i in range (0,40):
                    area = area + cv2.contourArea(nearStrip) + cv2.contourArea(farStrip)
                area = area /41
                dis = findDistance(area)
                area1 = cv2.contourArea(nearStrip) + cv2.contourArea(farStrip)
                #prints the distance to the center between the two strips
                print(dis)
                #draw the contours on the res display 
                cv2.drawContours(res, [nearStrip], 0, (0,0,255), 5)
                cv2.drawContours(res, [farStrip], 0, (255,0,0), 5)
        except cv2.error:
            print("no area to operate on!!!!!!!!!!")
        cv2.imshow('frame', frame)
        #cv2.imshow('mask', mask)
        cv2.imshow('res', res)
         # capture a keypress
        key = cv2.waitKey(20) & 0xFF
        # escape key
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    


if __name__ == "__main__":
    print(cv2.__version__)
    capture()

#TODO: write code for angle and then use networkTables