# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import numpy as np
import cv2
import picamera 
#import subprocess
import io
import logging
import math
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
    area = area + 5700
    dis = math.pow(area, -1.999)
    dis = dis * 4697990000
    dis = dis + 8
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
    #camera.start_preview()
    cap1 = cv2.VideoCapture(0)
    

    #camera.capture(stream, format='bgr')
    time.sleep(2)
    # adjust camera settings
    

    while(True):
        # Capture frame-by-frame
        
        _, frame = cap1.read()
    
    
        frame = cv2.GaussianBlur(frame, (11,11), 0)
        #data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        
        #frame = cv2.imdecode(data, 1)
        
        
        #operations on frame
        #
        #
        

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        
     
        
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
        
        res = cv2.bitwise_and(frame,frame, mask = mask) 

      
        
        _, cnts, _= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.imshow('cnts', cnts)
        #temp use gyro for angle of attack
        #IDK for angle of elevation
        #area = cv2.contourArea(cnts)
        #(area)
        #(np.array_str(calibration_box(frame)))
        
#         ret,thresh = cv2.threshold(mask,50,130,200)
#         contours,hierarchy = cv2.findContours(mask, 1, 2)
#         cnt = contours[0]
#         M = cv2.moments(cnt)
#          M
#         
#         rect = cv2.minAreaRect(cnt)
#         box = cv2.boxPoints(rect)
#         box = np.int0(box)
#         cv2.drawContours(img,[box],0,(0,0,255),2)
        try:
            if len(cnts) > 0:
                
                #a = max(cnts, key = cv2.contourArea)
                
                #area = cv2.contourArea(c)
                
                 
                c,d = findTargets(cnts)
                
                nearStrip = polygon(c)
                farStrip = polygon(d)    
                # Display the resulting frame 
                area = 0
                for i in range (0,40):
                    area = area + cv2.contourArea(nearStrip) + cv2.contourArea(farStrip)
                area = area /41
                dis = findDistance(area)
                area1 = cv2.contourArea(nearStrip) + cv2.contourArea(farStrip)
                
                print(area)
                cv2.drawContours(res, [nearStrip], 0, (0,0,255), 5)
                cv2.drawContours(res, [farStrip], 0, (255,0,0), 5)
        except cv2.error:
            print("no area to operate on!!!!!!!!!!")
        cv2.imshow('frame', frame)
        #cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        #cv2.imshow('cnt', cnts)
        #(res.centroid.x)
        #(res.centroid.y)
        
         # capture a keypress
        key = cv2.waitKey(20) & 0xFF
        # escape key
        if key == 27:
            break
    #camera.release()
    cv2.destroyAllWindows()
    #use find contures and use area


if __name__ == "__main__":
    
    print(cv2.__version__)
    
    capture()

