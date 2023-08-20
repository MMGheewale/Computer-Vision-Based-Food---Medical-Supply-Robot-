
###############################################################################
## Author: Team Supply Bot
## Edition: eYRC 2019-20
## Instructions: Do Not modify the basic skeletal structure of given APIs!!!
###############################################################################


######################
## Essential libraries
######################
import cv2
import numpy as np
import os
import math
import csv
import copy
import cv2.aruco as aruco
from xbee import XBee
from serial import Serial




############################################
## Build your algorithm in this function
## ip_image: is the array of the input image
## imshow helps you view that you have loaded
## the corresponding image
############################################

def process():                                                                          
    ###########################
    ## Your Code goes here
    ###########################
    cap = cv2.VideoCapture(1)                                                           # START VIDEO CAPTURE THROUGH WEBCAM 
    fps = cap.get(cv2.CAP_PROP_FPS)                                                     # GETTING THE FRAMES PER SECOND VALUE OF INPUT VIDEO
    cap.set(3, 640)                                                                     # SETTING THE VIDEO COUNTER TO FRAME SEQUENCE
    cap.set(4, 480)                                                                     # READING IN THE FRAME
    ret, frame = cap.read()
    cv2.imshow('realtime',frame)
    cv2.waitKey(int(1000/30));
    if(ret):                                                                            # VERIFYING FRAME HAS CONTENT
        ret, frame = cap.read()
        cv2.waitKey(int(1000/fps));
    image = frame
    img = image.copy()                                                                                                                               
    sample1 = image.copy()                                                              #TAKING COPY OF IMAGES TO WORK WITH ANGLE DETECTION
    original = image.copy()
    
    sector_image = np.zeros(image.shape[:3],np.uint8)*255                               #CREATING A BLACK IMAGE TO COPY REGION OF INTREST FOR CENTER CIRCLE DETECTION 
    B,G,R=cv2.split(image)                                                              
    X,Y,Z,=cv2.split(sector_image)
    i=132
    j=234
    while (i<307):                                                                      #COPYING REGION OF INTREST(PIXEL VALUE) TO BLACK IMAGE
        while (j<418): 
            X[i][j]=B[i][j]
            Y[i][j]=G[i][j]                                                             
            Z[i][j]=R[i][j]
            j+=1     
        i+=1
        j=234
    final_image=cv2.merge([X, Y, Z])
    final_image = cv2.medianBlur(final_image, 1)                                    
    hsvimg = cv2.cvtColor(final_image, cv2.COLOR_BGR2HSV)
    
    lower_range1 = np.array([0,0,142])                                              
    upper_range1 = np.array([180,30,255])                                             #here we are giving hsv to detect aruco center(white circle  
    mask1= cv2.inRange(hsvimg, lower_range1, upper_range1)
    masked1_DT = cv2.distanceTransform(mask1,cv2.DIST_L2,3)                           #Here we have used the func-Distance transform to get the actual foreground of the circles--
    ret, FG_IMG = cv2.threshold(masked1_DT,0.6*masked1_DT.max(),255,0)                #--doing this will increase the accuracy of the getting their centers as shrinking the circles-- 
    FG_IMG = np.uint8(FG_IMG)                                                         #--will bring us close to their centers
    sigma = 0.33
    v = np.median(FG_IMG)                                                             # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(FG_IMG, lower, upper)
    circles = cv2.HoughCircles(edged,  
    cv2.HOUGH_GRADIENT, 2, 10, param1 = 2,                                              #Here we are defining the parameters for detecting circles of our intrest 
    param2 =1, minRadius = 1, maxRadius = 2)
    if circles is not None:                                                                 #to ensure at least one white circle were found                                                    
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x1, y1, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(original, (x1, y1), r, (255, 0, 0), -1)
    cv2.circle(original, (int(x1), int(y1)), 350, (0, 0, 0), 440)
    cv2.circle(original, (int(x1), int(y1)), 100, (0, 0, 0), -1)                               
    gcopy = original.copy()
    
                                                                        
    red = cv2.medianBlur(original, 5)                                                           
    hsvimg = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
    lower_range1 = np.array([165,100,70])
    upper_range1 = np.array([180,255,255])

    mask1 = cv2.inRange(hsvimg, lower_range1, upper_range1)
    sigma = 0.33
    v = np.median(mask1)                                                            # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    edged1 = cv2.Canny(mask1, lower, upper)

    circles = cv2.HoughCircles(edged1,  
                       cv2.HOUGH_GRADIENT, 2, 10, param1 = 100,                     #Here we are defining the parameters for detecting circles of our intrest 
                   param2 =15, minRadius = 3, maxRadius = 8)
    if circles is not None:                                                         #check if red(Medical aid) circle detected                                                      
            Rstatus = True
            circles = np.round(circles[0, :]).astype("int")                         # convert the (x, y) coordinates and radius of the circles to integers
            # loop over the (x, y) coordinates and radius of the circles
            for (x2, y2, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(img, (x2, y2), r, (255, 0, 0), 2)
                    cv2.imshow("processing", img)
                    cv2.waitKey(int(1000/fps));
  
    if(Rstatus ==True):                                                             #verify medical aid detected
        PORT = 'COM8'
        BAUD = 9600
        ser = Serial(PORT, BAUD)                                                    #setup xbee communication
        xbee = XBee(ser)
        b = np.array([x1, y1])
        c = np.array([x2, y2])
        def capital_angle(a,b,c):                                                   #This function that calculate angle between capital,aruco center,and bot current position
            point_a = a - b
            point_b = c - b
            cosine_angle = np.dot(point_a, point_b) / (np.linalg.norm(point_a) * np.linalg.norm(point_b))
            ang_a = np.arctan2(*point_b[::-1])
            ang_b = np.arctan2(*point_a[::-1])
            angle= np.rad2deg((ang_a - ang_b) % (2 * np.pi))                                          
            return angle
        def bot_center(ima,i):                                                                                   #function that detects aruco center and also calculate angle between                                         
            aruco_list = {}                                                                                      #angle between red coin ,aruco center,and bot current position
            gray = cv2.cvtColor(ima, cv2.COLOR_BGR2GRAY)                                
            aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)                                                 #creating aruco_dict with 5x5 bits with max 250 ids..so ids ranges from 0-249
            img = ima.copy()
            parameters = aruco.DetectorParameters_create()                                                       
            corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)                     #lists of ids and the corners beloning to each id
           #corners is list of corners(numpy array) of the detected markers. For each marker,its four corners are returned in their original order(which is clockwise starting with top left)
            gray = aruco.drawDetectedMarkers(gray, corners,ids)                         #. So, the first corner is the top left corner, followed by the top right, bottom right and bottom left.
            if len(corners):                                                            #returns no of arucos
                for k in range(len(corners)):
                    temp_1 = corners[k]
                    temp_1 = temp_1[0]
                    temp_2 = ids[k]
                    temp_2 = temp_2[0]
                    aruco_list[temp_2] = temp_1
            key_list = aruco_list.keys()
            font = cv2.FONT_HERSHEY_SIMPLEX
            try:                                                                                            #try block to check if aruco not detected deblur the image and then detect aruco 
                def angle_calculate(pt1,pt2, trigger = 0):  # function which returns angle between two points in the range of 0-359
                    angle_list_1 = list(range(359,0,-1))
                    #angle_list_1 = angle_list_1[90:] + angle_list_1[:90]
                    angle_list_2 = list(range(359,0,-1))
                    angle_list_2 = angle_list_2[-90:] + angle_list_2[:-90]
                    x=pt2[0]-pt1[0] # unpacking tuple
                    y=pt2[1]-pt1[1]
                    angle=int(math.degrees(math.atan2(y,x))) #takes 2 points nad give angle with respect to horizontal axis in range(-180,180)
                    if trigger == 0:
                        angle = angle_list_2[angle]
                    else:
                        angle = angle_list_1[angle]
                    return int(angle)
                for key in key_list:
                    dict_entry = aruco_list[key]                                                            #dict_entry is a numpy array with shape (4,2)
                    centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]         
                    centre[:] = [int(x / 4) for x in centre]                                                #finding the centre
                    orient_centre = centre + [0.0,5.0]
                    centredraw = tuple(centre)  
                    orient_centre = tuple((dict_entry[0]+dict_entry[1])/2)
                    cv2.circle(img,centredraw,1,(0,0,255),8)
                    cv2.circle(img,tuple(dict_entry[0]),1,(0,0,255),8)
                    cv2.circle(img,tuple(dict_entry[1]),1,(0,255,0),8)
                    cv2.circle(img,tuple(dict_entry[2]),1,(255,0,0),8)
                    cv2.circle(img,orient_centre,1,(0,0,255),8)
                    if(i==1 or i==2):
                        cv2.circle(img, (x2, y2), r, (255, 0, 0), 2)
                        text1 = "One instance of Medical Aid detected"
                        font1 = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(img,text1,(50,50), font1 , 0.5,(0,0,255),1,cv2.LINE_AA)
                    cv2.line(img,centredraw,orient_centre,(255,0,0),4) #marking the centre of aruco
                    cv2.putText(img, str(key), (int(centredraw[0] + 20), int(centredraw[1])), font, 1, (0,0,255), 2, cv2.LINE_AA) # displaying the idn
                    robot_state = {}
                    key_list = aruco_list.keys()
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    for key in key_list:
                        dict_entry = aruco_list[key]
                        pt1 , pt2 = tuple(dict_entry[0]) , tuple(dict_entry[1])
                        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]
                        centre[:] = [int(x / 4) for x in centre]
                        centre = tuple(centre)
                        angle = angle_calculate(pt1, pt2)
                        cv2.putText(img, str(angle), (int(centre[0] - 80), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA)
                    cv2.imshow("processing", img)
                    cv2.waitKey(int(1000/fps));
                    c1,c2=centre  
                    center1=int(c1)
                    center2=int(c2)    
                    a = np.array([center1, center2])
            except:
                print("error")
                ret, frame = cap.read()
                bot_center(frame,5)
            point_a = a - b
            point_b = c - b
            np.seterr(divide='ignore',invalid='ignore')
            cosine_angle = np.dot(point_a, point_b) / (np.linalg.norm(point_a) * np.linalg.norm(point_b))   #calculate angle between bot,aruco center, medical aid in clock wise direction
            ang_a = np.arctan2(*point_b[::-1])
            ang_b = np.arctan2(*point_a[::-1])
            angle= np.rad2deg((ang_a - ang_b) % (2 * np.pi))                                               #angle between red coin ,aruco center,and bot current position
            if(i==0):
                i=4
                init_angle=np.array([center1, center2])                                                                              #store position of the capital ie bot standing at capital 
                if(angle<45):
                    print("The city at node 2 requires medical aid")
                elif(angle<90):
                    print("The city at node 3 requires medical aid")
                elif(angle<135):
                    print("The city at node 4 requires medical aid")
                elif(angle<180):
                    print("The city at node 5 requires medical aid")
                elif(angle<200):
                    print("The city at node 6 requires medical aid")
                elif(angle<250):
                    print("The city at node 7 requires medical aid")
                elif(angle<300):
                    print("The city at node 8 requires medical aid")
                elif(angle<360):
                    print("The city at node 9 requires medical aid")
            if(i==1 or i==2):
                return int(angle)
            if(i==3):
                return a                                                                                   #returns angle when bot is moving forward or backward   
            if(angle<=180):                                                                                #finding shortest route from capital to medical aid and goes forward or backward
                i=1
                print("forward")
                xbee.tx(dest_addr='\x00\x01', data='f')
                reached=0
                while(reached==0):
                    ret, frame = cap.read()
                    cv2.imshow("video camera stream", frame)
                    cv2.waitKey(int(1000/fps));
                    angle= bot_center(frame,1)
                    if(angle<=10):                                                                       #give stop signal to bot through xbee to stop in front medical aid
                        xbee.tx(dest_addr='\x00\x01', data='s')
                        reached=1
                        completed=0
                        while(completed==0):
                            ret, frame = cap.read()
                            a= bot_center(frame,3)
                            cap_angle=capital_angle(a,b,init_angle)
                            if(cap_angle<=5):                                                           #now when bot starts going back to capital send stop signal to bot signal  
                                xbee.tx(dest_addr='\x00\x01', data='s')
                                exit()
            else:
                i=2
                print("backward")
                xbee.tx(dest_addr='\x00\x01', data='b')
                reached=0
                while(reached==0):
                    ret, frame = cap.read()
                    ## display to see if the frame is correct
                    cv2.imshow("video camera stream", frame)
                    cv2.waitKey(int(1000/fps));
                    angle= bot_center(frame,i)
                    if(360-angle<=10):                                                                  #give stop signal to bot through xbee to stop in front medical aid
                        xbee.tx(dest_addr='\x00\x01', data='s')
                        reached=1
                        completed=0
                        while(completed==0):
                            ret, frame = cap.read()
                            a= bot_center(frame,3)
                            cap_angle=capital_angle(a,b,init_angle)
                            if(cap_angle<=10):                                                           #now when bot starts going back to capital send stop signal to bot signal 
                                xbee.tx(dest_addr='\x00\x01', data='s')
                                exit()
        ret, frame = cap.read()                                                                        #read frame and sends to bot_center function to calculate angle between 
        bot_center(frame,0)                                                                            #bot, aruco center, and medical aid
    else:
        Rstatus = False                                                                                #set red circle detection not detected 
    return sample1
    
    
####################################################################
## The main program which provides read in input of one image at a
## time to process function in which you will code your generalized
## output computing code
## Modify the image name as per instruction
####################################################################
def main():
    ################################################################
    ## variable declarations
    ################################################################
    op_image = process()
    cv2.imwrite("SB#9999_task3I.jpg",op_image)

    

############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main()
