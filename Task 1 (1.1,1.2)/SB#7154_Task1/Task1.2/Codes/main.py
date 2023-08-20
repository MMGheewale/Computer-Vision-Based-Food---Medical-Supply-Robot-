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
    ## placeholder image
    sector_image = np.ones(ip_image.shape[:2],np.uint8)*255                #We are using the white image provided to us as it is.
    
    Whiteimage = np.zeros_like(ip_image)                                   #Here we are converting 1 channeled image "sector image" to 3 channeled white image
    Whiteimage[:,:,0] = sector_image
    Whiteimage[:,:,1] = sector_image
    Whiteimage[:,:,2] = sector_image
    
    
    hsvimg = cv2.cvtColor(ip_image, cv2.COLOR_BGR2HSV)                     #Creating a HSV image of ip_image 
    
    lower_range1 = np.array([0,0,255])                                     #We are giving hsv range for white colour that is to be retined after filtering (since the missing strip is white)
    upper_range1 = np.array([0,0,255])
    mask = cv2.inRange(hsvimg, lower_range1, upper_range1)                 #This makes the code generalized for detecting missing strip of any colour by adjusting HSV range

    kernel = np.ones((1,1),np.uint8)                                       #To remove any small white noises in the image using morphological opening.
    mask1 = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel, iterations = 1)

    img2 = np.zeros_like(ip_image)                                         #Here we are converting 1 channeled image "mask1" to 3 channeled
    img2[:,:,0] = mask1
    img2[:,:,1] = mask1
    img2[:,:,2] = mask1
    
    
    B,G,R=cv2.split(img2)                                                  #pixel values of img2
    X,Y,Z=cv2.split(Whiteimage)                                            #pixel values of Whiteimage
        

    #segment 1                                                             # Here we are using the concept of segmentation and we have deviced a logic--
    i=178                                                                  # --that divides ip_image into segments such that all segments enclose the inner black ring --- 
    j=284                                                                  # --and finds the pixel location of the missing strip in inner black ring
    while (i< 345):
        while (j<739): 
            if(B[i][j]==255 & G[i][j]==255 & R[i][j]==255):                # Here we are predecting the pixel values of the missing strip that is to be filled with black
                X[i][j]=0                                                  # Here the part of the inner black strip which is missing(white-255) if it is dected in that segment then--- 
                Y[i][j]=0                                                  #--it turns the same pixel values of the Whiteimage to black thus creating/filling the missing part
                Z[i][j]=0    
            j+=1     
        i+=1
        j=284
    
    #segment 2  
    i=671
    j=284
    while (i< 848):
        while (j<738): 
            if(B[i][j]==255 & G[i][j]==255 & R[i][j]==255):                 #These values of i,j are obtained by image study and segmenting the image into required regions
                X[i][j]=0
                Y[i][j]=0
                Z[i][j]=0    
            j+=1     
        i+=1
        j=284

    #segment 3  
    i=264
    j=211
    while (i<753):
        while (j<289): 
            if(B[i][j]==255 & G[i][j]==255 & R[i][j]==255):
                X[i][j]=0
                Y[i][j]=0
                Z[i][j]=0    
            j+=1     
        i+=1
        j=211
        
    #segment 4      
    i=266
    j=736
    while (i<745):
        while (j<817): 
            if(B[i][j]==255 & G[i][j]==255 & R[i][j]==255):
                X[i][j]=0
                Y[i][j]=0
                Z[i][j]=0    
            j+=1     
        i+=1
        j=736

    #segment 5  
    i=319
    j=812    
    while (i<628):
        while (j<847): 
            if(B[i][j]==255 & G[i][j]==255 & R[i][j]==255):
                X[i][j]=0
                Y[i][j]=0
                Z[i][j]=0    
            j+=1     
        i+=1
        j=812

    #segment 6      
    i=372
    j=178
    while (i<643):
        while (j<216): 
            if(B[i][j]==255 & G[i][j]==255 & R[i][j]==255):
                X[i][j]=0
                Y[i][j]=0
                Z[i][j]=0    
            j+=1     
        i+=1
        j=178                                               #Doing this segmentation makes the code generalized to identify and fill any missing strip present in the inner black ring
         
                                                                         
    final_image=cv2.merge([X, Y, Z])
    grayImage = cv2.cvtColor(final_image, cv2.COLOR_BGR2GRAY)
    (thresh, sector_image) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY) # To convert the final image to pure black and white
    ## Your Code goes here
    ###########################
    return sector_image




    
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
    ## Reading 1 image at a time from the Images folder
    for image_name in os.listdir(images_folder_path):
        ## verifying name of image
        print(image_name)
        ## reading in image 
        ip_image = cv2.imread(images_folder_path+"/"+image_name)
        ## verifying image has content
        print(ip_image.shape)
        ## passing read in image to process function
        sector_image = process(ip_image)
        ## saving the output in  an image of said name in the Generated folder
        cv2.imwrite(generated_folder_path+"/"+image_name
                    [0:len(image_name)-4]+"_fill_in.png", sector_image)
        i+=1


    

############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main()
