# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import numpy as n
import cv2
<<<<<<< HEAD
import picamera
=======
#from picamera import PiCamera
>>>>>>> 3643d91d10344968b0a0fc11827737f6faf43c8d
import os
import logging
logging.basicConfig(level=logging.DEBUG)

def capture():
<<<<<<< HEAD
    camera = picamera.PiCamera()
=======
    #camera = PiCamera()
>>>>>>> 3643d91d10344968b0a0fc11827737f6faf43c8d
    cap = cv2.VideoCapture(0)
    while(True):
        # Capture frame-by-frame
        frame = cap.read()
        
        
        #operations on frame
        #
        #
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lowerGreen = n.array([45,54,55])
        
        higherGreen = n.array([75,255,255])
        
        mask = cv2.inRange(hsv,lowerGreen,higherGreen)
        
        res = cv2.bitwise_and(frame,frame, mask = mask) 
        
        #temp use gyro for angle of attack
        #IDK for angle of elevation
        
        
        # Display the resulting frame 
        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        print(res.centroid.x)
        print(res.centroid.y)
        cv2.waitKey(20) & 0xFF == ord('q')
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    #use find contures and use area

def setup():
    os.system("source ~/.profile")
    os.system("worknon cv")

if __name__ == "__main__":
    print("Hello World")
    print(cv2.__version__)
    capture()

