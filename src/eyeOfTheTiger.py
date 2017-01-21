# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import numpy as np
import cv2
import picamera 
import os
import io
import logging
import time
logging.basicConfig(level=logging.DEBUG)

def capture():


    stream = io.BytesIO() 

    camera = picamera.PiCamera()
    
    camera.start_preview()

    

    camera.capture(stream, format='jpeg')
    time.sleep(2)
    # adjust camera settings
    

    while(True):
        # Capture frame-by-frame
        
    
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        ret = True
        frame = cv2.imdecode(data, 1)
        
        
        #operations on frame
        #
        #
        

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lowerGreen = np.array([45,54,55])
        
        higherGreen = np.array([75,255,255])
        
        mask = cv2.inRange(hsv,lowerGreen,higherGreen)
        
        #res = cv2.bitwise_and(frame,frame, mask = mask) 
        
        #temp use gyro for angle of attack
        #IDK for angle of elevation
        
        
        # Display the resulting frame 
        #cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)

        #cv2.imshow('res', res)
        #print(res.centroid.x)
        #print(res.centroid.y)
        
         # capture a keypress
        key = cv2.waitKey(20) & 0xFF
        # escape key
        if key == 27:
            break
    cap.release()
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

