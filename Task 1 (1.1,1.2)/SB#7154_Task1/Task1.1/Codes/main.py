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




########################################################################
## using os to generalise Input-Output
########################################################################
codes_folder_path = os.path.abspath('.')
images_folder_path = os.path.abspath(os.path.join('..', 'Images'))
generated_folder_path = os.path.abspath(os.path.join('..', 'Generated'))




############################################
## Build your algorithm in this function
## ip_image: is the array of the input image
## imshow helps you view that you have loaded
## the corresponding image
############################################
def process(ip_image):
    ###########################
    ## Your Code goes here
       
    hsvimg = cv2.cvtColor(ip_image, cv2.COLOR_BGR2HSV)              

    lower_range1 = np.array([60,255,255])
    upper_range1 = np.array([60,255,255])
    mask1 = cv2.inRange(hsvimg, lower_range1, upper_range1)                      #Filtering the hsvimg except green dot to avoid any other colour dot to be detcected
    
    lower_range2 = np.array([0,255,255])
    upper_range2 = np.array([0,255,255])
    mask2 = cv2.inRange(hsvimg, lower_range2, upper_range2)                      #Filtering the hsvimg except red dot to avoid any other colour dot to be detcected


    masked = cv2.add(mask1,mask2)
    
    kernel = np.ones((2,1),np.uint8)                                             #To remove any small white noises in the image using morphological opening.
    masked1 = cv2.morphologyEx(masked,cv2.MORPH_OPEN,kernel, iterations = 3)
    
    kernel = np.ones((1,1),np.uint8) 
    masked1 = cv2.morphologyEx(masked1,cv2.MORPH_CLOSE,kernel, iterations = 1)   #To remove any small holes (if any) in the image using morphological closing.
      
   
    masked1_DT = cv2.distanceTransform(masked1,cv2.DIST_L2,5)                    #Here we have used the func-Distance transform to get the actual foreground of the circles--
    ret, FG_IMG = cv2.threshold(masked1_DT,0.8*masked1_DT.max(),255,0)           #--doing this will increase the accuracy of the getting their centers as shrinking the circles-- 
    FG_IMG = np.uint8(FG_IMG)                                                    #--will bring us close to their centers
    
    result = cv2.bitwise_and(ip_image,ip_image, mask = FG_IMG)
    
                                                                # The above part of code ensures that variable "result" has exactly two dots i.e red and green coloured, 
                                                                # We have made the code generalized to find the angle b/w any two specific coloured dots--
                                                                #--which can be done by just adjusting the HSV range accordingly with the colour of the dot.
                                                                
    grayimg = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY) 
    
     
    g_b = cv2.blur(grayimg, (1, 1))                                              #To remove further noise
    
  
    d_circles = cv2.HoughCircles(g_b,  
                       cv2.HOUGH_GRADIENT, 2, 1, param1 = 2,                     #Here we are defining the parameters for detecting circles of our intrest 
                   param2 =1, minRadius = 1, maxRadius = 40)                     #--using Hough transform on the blurred image.
       
 
    if d_circles is not None: 
        d_circles = np.uint16(np.around(d_circles)) 
        i=0
        u=int(ip_image.shape[0])/2                                                # To find the center of the ip_image and assigned to variables "u","v"--
        v=int(ip_image.shape[1])/2                                                #--because the center lies at the centre of the ip_image
        
        for pt in d_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2]                                         # This gives the center cordinates and radius of the detected dots 
            if(i==0):                                                                               
                w=a
                x=b
            if(i==1):
                y=a
                z=b
            i+=1


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
  
    angle=Angle((int(w),int(x)),(int(u),int(v)),(int(y),int(z)))
    angle= round(angle,2)
    return angle




    
####################################################################
## The main program which provides read in input of one image at a
## time to process function in which you will code your generalized
## output computing code
## Do not modify this code!!!
####################################################################
def main():
    ################################################################
    ## variable declarations
    ################################################################
    i = 1
    line = []
    ## Reading 1 image at a time from the Images folder
    for image_name in os.listdir(images_folder_path):
        ## verifying name of image
        print(image_name)
        ## reading in image 
        ip_image = cv2.imread(images_folder_path+"/"+image_name)
        ## verifying image has content
        print(ip_image.shape)
        ## passing read in image to process function
        A = process(ip_image)
        ## saving the output in  a list variable
        line.append([str(i), image_name , str(A)])
        ## incrementing counter variable
        i+=1
    ## verifying all data
    print(line)
    ## writing to angles.csv in Generated folder without spaces
    with open(generated_folder_path+"/"+'angles.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(line)
    ## closing csv file    
    writeFile.close()



    

############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main()
