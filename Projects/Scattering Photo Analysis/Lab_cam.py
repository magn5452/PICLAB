# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:20:32 2023

@author: Frederik P, Frederik S
"""

# import the opencv library
import cv2
import time
import matplotlib.pyplot as plt

class Camera:
    
    def __init__(self, device_number=0):
        self.__video_capture = cv2.VideoCapture(device_number)        

    
    def __del__(self):
        self.__video_capture.release()


    def capture(self, filename=None):
       # Capture the video frame

       ret, frame = self.__video_capture.read()
       frame = cv2.flip(frame,0)
       frame = cv2.flip(frame,1)
       cv2.waitKey(1)
       if ret:
           if filename != None:
               cv2.imwrite(filename, frame)     # save frame as JPEG file
           return frame
       else:
           raise Exception("No Image frame acquired") 
    
    def camsetup(self,width=2448,height=2048):
        #self.__video_capture.set(cv2.CAP_PROP_SETTINGS, 1)
        self.__video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.__video_capture.set(cv2.CAP_PROP_SETTINGS,1)
        if not self.__video_capture.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # Capture frame-by-frame
            ret, frame = self.__video_capture.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            frame = cv2.flip(frame,0)
            frame = cv2.flip(frame,1)
            resized_frame = cv2.resize(frame, (1600, 900))   
            cv2.imshow('frame', resized_frame)
            
            if cv2.waitKey(1) == ord('q'):
                break
        # When everything done, release the capture
        cv2.destroyAllWindows()


def main():
                
    device_number = 1
    cam1 = Camera(device_number)
    
    
    cam1.camsetup()
    frame = cam1.capture("test.jpg")
    plt.figure()
    plt.imshow(frame)

    
    cv2.destroyAllWindows()
    cam1.__del__()
    
if __name__ == "__main__":
    main()
