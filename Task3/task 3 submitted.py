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






############################################
## Build your algorithm in this function
## ip_image: is the array of the input image
## imshow helps you view that you have loaded
## the corresponding image
############################################

def process(ip_image):
    ###########################
    ## Your Code goes here
    ###########################
    try:
        image = ip_image
        sample = image.copy()
        sample1 = image.copy()
        original = image.copy()

        sector_image = np.zeros(image.shape[:3],np.uint8)*255

        B,G,R=cv2.split(image)
        X,Y,Z,=cv2.split(sector_image)
        i=132
        j=234
        while (i<307):
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
        upper_range1 = np.array([180,30,255])
        mask1= cv2.inRange(hsvimg, lower_range1, upper_range1)


        masked1_DT = cv2.distanceTransform(mask1,cv2.DIST_L2,3)                      #Here we have used the func-Distance transform to get the actual foreground of the circles--
        ret, FG_IMG = cv2.threshold(masked1_DT,0.6*masked1_DT.max(),255,0)           #--doing this will increase the accuracy of the getting their centers as shrinking the circles-- 
        FG_IMG = np.uint8(FG_IMG)                                                    #--will bring us close to their centers




        sigma = 0.33
        v = np.median(FG_IMG)


        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        edged = cv2.Canny(FG_IMG, lower, upper)


        circles = cv2.HoughCircles(edged,  
                           cv2.HOUGH_GRADIENT, 2, 10, param1 = 2,                     #Here we are defining the parameters for detecting circles of our intrest 
                       param2 =1, minRadius = 1, maxRadius = 2)

         
        # ensure at least some circles were found
        if circles is not None:
                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
         
                # loop over the (x, y) coordinates and radius of the circles
                for (x1, y1, r) in circles:
                        # draw the circle in the output image, then draw a rectangle
                        # corresponding to the center of the circle
                        cv2.circle(original, (x1, y1), r, (255, 0, 0), -1)
                
        #print (int(x1), int(y1))

        cv2.circle(original, (int(x1), int(y1)), 350, (0, 0, 0), 400)
        cv2.circle(original, (int(x1), int(y1)), 100, (0, 0, 0), -1)

        gcopy = original.copy()

        red = cv2.medianBlur(original, 5)

        hsvimg = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
        lower_range1 = np.array([165,100,70])
        upper_range1 = np.array([180,255,255])

        mask1 = cv2.inRange(hsvimg, lower_range1, upper_range1)

        sigma = 0.33
        v = np.median(mask1)


        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        edged1 = cv2.Canny(mask1, lower, upper)

        circles = cv2.HoughCircles(edged1,  
                           cv2.HOUGH_GRADIENT, 2, 10, param1 = 100,                     #Here we are defining the parameters for detecting circles of our intrest 
                       param2 =15, minRadius = 3, maxRadius = 8)

         
        # ensure at least some circles were found
        if circles is not None:
                Rstatus = True
                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
         
                # loop over the (x, y) coordinates and radius of the circles
                for (x2, y2, r) in circles:
                        # draw the circle in the output image, then draw a rectangle
                        # corresponding to the center of the circle
                        cv2.circle(sample, (x2, y2), r, (255, 0, 0), 2)
                        
        else:
                Rstatus = False
        
       # print (int(x2), int(y2))

        green = cv2.medianBlur(gcopy, 7)

        hsvimg = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)
        lower_range1 = np.array([20,30,50])
        upper_range1 = np.array([50,255,255])

        mask1 = cv2.inRange(hsvimg, lower_range1, upper_range1)

        sigma = 0.33
        v = np.median(mask1)


        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        edged1 = cv2.Canny(mask1, lower, upper)

        circles = cv2.HoughCircles(edged1,  
                           cv2.HOUGH_GRADIENT, 2, 10, param1 = 100,                     #Here we are defining the parameters for detecting circles of our intrest 
                       param2 =15, minRadius = 3, maxRadius = 8)

        def Angle(m, n, o):                                                                             # This function finds the angle between two points--
            ang = math.degrees(math.atan2(o[1]-n[1], o[0]-n[0]) - math.atan2(m[1]-n[1], m[0]-n[0]))     # --taking the center of the ip_image as origin 
            if(ang<0):                                                                                  
                ang1 = ang*-1                                                                               
                if(ang1<=180):
                    return ang1                                                         # This part ensures that the ouput angle is +ve & is the included angle b/w the two dots
                else:                                                                   # so here o/p angle can be either 180 or less than that(included of the dots & not exterior)
                    ang2 = 360-ang1                                                                                                     
                    return ang2
                
            elif(ang<=180):
                return ang
                
            else:
                ang2 = 360-ang
                return ang2 
        # ensure at least some circles were found
        if circles is not None:
                i =1
                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")

            
                # loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                        # draw the circle in the output image, then draw a rectangle
                        # corresponding to the center of the circle
                        cv2.circle(sample, (x, y), r, (255, 0, 0), 2)
                        
                        if (i == 1):
                            G1status = True
                            x3 = x
                            y3 = y 
                            i+=1
                            G2status = False
                           
                        else:
                            G2status = True
                            x4 = x
                            y4 = y

                    
        
        
        else:
             G1status = False
             G2status = False

        
        
                            
        if (Rstatus == True and G1status == False):
                text = "Angle: 0  (One instance of Medical Aid detected) "
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(sample,text,(50,50), font , 0.5,(0,0,255),1,cv2.LINE_AA)

        if (Rstatus == False and G1status == True and G2status == False):
                text = "Angle: 0: (One instance of Food Supply detected) "
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(sample,text,(50,50), font , 0.5,(0,0,255),1,cv2.LINE_AA)
                
        if (Rstatus == True and G1status == True and G2status == False):
                angle=Angle((int(x2),int(y2)),(int(x1),int(y1)),(int(x3),int(y3)))
                angle= round(angle,2)
                text = "Angle: "+str(angle)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(sample,text,(50,50), font , 0.5,(0,0,255),1,cv2.LINE_AA)
                
        if (Rstatus == False and G1status == True and G2status == True):
                angle=Angle((int(x3),int(y3)),(int(x1),int(y1)),(int(x4),int(y4)))
                angle= round(angle,2)
                text = "Angle: "+str(angle)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(sample,text,(50,50), font , 0.5,(0,0,255),1,cv2.LINE_AA)
                
        if (Rstatus == True and G1status == True and G2status == True):
                angle1=Angle((int(x2),int(y2)),(int(x1),int(y1)),(int(x3),int(y3)))
                angle1= round(angle1,2)
                
                angle2=Angle((int(x2),int(y2)),(int(x1),int(y1)),(int(x4),int(y4)))
                angle2= round(angle2,2)
                
                if (angle1>angle2):
                    amax = angle1
                    amin = angle2
                    
                else:
                    
                    if (angle1<angle2):
                        amax = angle2
                        amin = angle1

                    else:
                        amax = amin
                        text  = "Angle max = Angle min: "+str(amax)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(sample,text,(50,50), font , 0.5,(0,0,255),1,cv2.LINE_AA)

                text1 = "Angle max: "+str(amax)
                text2 = "Angle min: "+str(amin)
                text  = "Angles measured with Medical aid as reference"
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(sample,text,(50,20), font , 0.5,(0,0,255),1,cv2.LINE_AA)
                cv2.putText(sample,text1,(50,45), font , 0.5,(0,0,255),1,cv2.LINE_AA)
                cv2.putText(sample,text2,(50,65), font , 0.5,(0,0,255),1,cv2.LINE_AA)

                
        elif(Rstatus == False and G1status == False and G2status == False):
                text  = "Absence of Relief aids"
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(sample,text,(50,50), font , 0.5,(0,0,255),1,cv2.LINE_AA)
        
        
        cv2.imshow("output", sample)
        



        return sample

    except:
       return ip_image
    
    
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
    i = 1
    ## reading in video 
    cap = cv2.VideoCapture(1) #if you have a webcam on your system, then change 0 to 1
    ## getting the frames per second value of input video
    fps = cap.get(cv2.CAP_PROP_FPS)
    ## setting the video counter to frame sequence
    cap.set(3, 640)
    cap.set(4, 480)
    ## reading in the frame
    ret, frame = cap.read()
    ## verifying frame has content
    print(frame.shape)
    while(ret):
        ret, frame = cap.read()
        ## display to see if the frame is correct
        cv2.imshow("window", frame)
        cv2.waitKey(int(1000/fps));
        ## calling the algorithm function
        op_image = process(frame)
        cv2.imwrite("SB#9999_task3I.jpg",op_image)


    

############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main()
