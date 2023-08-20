import cv2
import numpy as np
import os

#The following function extracts the frame from from the given video at time=6 sec
def partA():
    videopathA = cv2.VideoCapture('..\\Videos\\RoseBloom.mp4')
    videopathA.set(cv2.CAP_PROP_POS_MSEC,6000)      
    status,image = videopathA.read()
    if status:
        cv2.imwrite('..\\Generated\\frame_as_6.jpg', image)
        
#The following function visualizes the red component of the frame extracted above where blue and green components are set to zero           
def partB():
    imgpathB="..\\Generated\\frame_as_6.jpg"
    imgB =cv2.imread(imgpathB)
    B,G,R=cv2.split(imgB)
    zeros=np.zeros(imgB.shape[:2],dtype="uint8")
    newimgB=cv2.merge([zeros,zeros,R])
    cv2.imwrite('..\\Generated\\frame_as_6_red.jpg',newimgB)

#Calling the above functions
partA()
partB()

