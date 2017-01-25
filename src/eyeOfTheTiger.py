# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import numpy as np
import cv2
import picamera 
import os
import io
import logging


logging.basicConfig(level=logging.DEBUG)


LOWER_GREEN = np.array([30, 20, 20])
UPPER_GREEN = np.array([70, 230, 230])

# Calibration box dimensions
CAL_AREA = 1600
CAL_SIZE = int(math.sqrt(CAL_AREA))
CAL_UP = FRAME_CY + (CAL_SIZE / 2)
CAL_LO = FRAME_CY - (CAL_SIZE / 2)
CAL_R = FRAME_CX - (CAL_SIZE / 2)
CAL_L = FRAME_CX + (CAL_SIZE / 2)
CAL_UL = (CAL_L, CAL_UP)
CAL_LR = (CAL_R, CAL_LO)


def calibration_box(img):
    """Return HSV color in the calibration box."""
    cv2.rectangle(img, CAL_UL, CAL_LR, (0, 255, 0), thickness=1)
    roi = img[CAL_LO:CAL_UP, CAL_R:CAL_L]
    average_color_per_row = np.average(roi, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    average_color = np.uint8([[average_color]])
    hsv = cv2.cvtColor(average_color, cv2.COLOR_BGR2HSV)
    return hsv


def capture():
    #stream = io.BytesIO() 
    
    #camera = picamera.PiCamera()
    
    #camera.start_preview()
    cap1 = cv2.VideoCapture(0)
    

    #camera.capture(stream, format='bgr')
    time.sleep(2)
    # adjust camera settings
    
    while(True):
        # Capture frame-by-frame
        
        _, frame1 = cap1.read()
    
        #data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        
        #frame = cv2.imdecode(data, 1)
        
        
        #operations on frame
        #
        #
        
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        
       
        
        mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
        
        res = cv2.bitwise_and(frame,frame, mask = mask) 
        
        #temp use gyro for angle of attack
        #IDK for angle of elevation
        print(np.array_str(calibration_box(frame)))
        cv2.imshow("NerdyCalibration", frame)
        
        contours,hierarchy = cv2.findContours(mask, 1, 2)
        cnt = contours[0]
        M = cv2.moments(cnt)
        print M
        
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img,[box],0,(0,0,255),2)
        # Display the resulting frame 
        cv2.imshow('frame', frame1)
        #cv2.imshow('mask', mask)
        #cv2.imshow('res', res)
        #print(res.centroid.x)
        #print(res.centroid.y)
        
         # capture a keypress
        key = cv2.waitKey(20) & 0xFF
        # escape key
        if key == 27:
            break
    #camera.release()
    cv2.destroyAllWindows()
    #use find contures and use area

def setup():
    os.system("cd /")
    os.system("source ~/.profile")
    os.system("worknon cv")

if __name__ == "__main__":
    print("Hello World")
    print(cv2.__version__)
    setup()
    capture()

