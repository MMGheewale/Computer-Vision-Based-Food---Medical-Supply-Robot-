import numpy as np
import cv2
import cv2.aruco as aruco
from aruco_lib import *

robot_state=0
det_aruco_list = {}

def detect(frame):                                                              #Defining the function detect and calling it from main.py to return the marked image with ID and angle  
	det_aruco_list = detect_Aruco(frame)                                    #Checking if aruco code is present in the image and thenif yes we enter into the if statement
	
	if det_aruco_list:
		img = mark_Aruco(frame,det_aruco_list)                          #Sending the revelant info to aruco.lib to do the marking 
		robot_state = calculate_Robot_State(img,det_aruco_list)         #Sending the revelant info to aruco.lib to know the robot state with appropriate (ID & Angle)
		a= robot_state.values()                                         #taking the returned values into a 
		b=str(a)                                                        #Converting a into string and assigning it to b
		output = b.split(', ')                                          #Spliting the string to get o/p in list format
		output[0]=str(output[0]).strip('dict_values([[')                #Taking specific values from output and reassigning it to [0] th, [3]rd position in that list
		output[3]=str(output[3]).strip(']])')
		cv2.circle(img,(255,50),1,(0,255,0),2)                         
		cv2.imshow('marker', img)
		cv2.imwrite("..//Generated//aruco_with_id.png",img)             #Writing the image with id and angle into generated folder
		return output



	


