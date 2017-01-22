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



LOWER_BLUE = np.array([110,50,50], dtype=np.uint8)
UPPER_BLUE = np.array([130,255,255], dtype=np.uint8)


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
        
        frame = cv2.imdecode(data, 1)
        
        
        #operations on frame
        #
        #
        

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
       
        
        mask = cv2.inRange(hsv, LOWER_BLUE, UPPER_BLUE)
        
        #res = cv2.bitwise_and(frame,frame, mask = mask) 
        
        #temp use gyro for angle of attack
        #IDK for angle of elevation
        
        
        # Display the resulting frame 
        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)

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

