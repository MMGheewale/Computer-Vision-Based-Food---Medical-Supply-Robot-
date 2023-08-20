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
import cv2.aruco as aruco
from aruco_lib import *
import copy
import aruco_detection                                                              #Importing the aruco_detection code from codes folder 


########################################################################
## using os to generalise Input-Output
########################################################################
codes_folder_path = os.path.abspath('.')
images_folder_path = os.path.abspath(os.path.join('..', 'Videos'))
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
    ###########################
    id_list = []
    
    def Blurly_edge(image, d=31):                                                  #Defining a function blurly_edge and appling gausian blur to basically correct the blurry edges in later 
        h, w  = image.shape[:2]                                                    #*Stage of filtering
        image_pad = cv2.copyMakeBorder(image, d, d, d, d, cv2.BORDER_WRAP)
        image_blur = cv2.GaussianBlur(image_pad, (2*d+1, 2*d+1), -1)[d:-d,d:-d]
        y, x = np.indices((h, w))
        dist = np.dstack([x, w-x-1, y, h-y-1]).min(-1)
        w = np.minimum(np.float32(dist)/d, 1.0)
        return image*w + image_blur*(1-w)

    def motion_kernel(anglele, length, sz=20):                                      #Algorithm to create and simulate a similar motionblur PSF kernel, we pass PSF(angle,length,Matrix_size)
        kernel = np.ones((1, length), np.float32)
        c, s = np.cos(anglele), np.sin(anglele)
        B = np.float32([[c, -s, 0], [s, c, 0]])
        sz2 = sz // 2
        B[:,2] = (sz2, sz2) - np.dot(B[:,:2], ((length-1)*0.5, 0))
        kernel = cv2.warpAffine(kernel, B, (sz, sz), flags=cv2.INTER_CUBIC)
        return kernel


    im_gray = cv2.cvtColor(ip_image, cv2.COLOR_BGR2GRAY)                                    #Making a gray image using ip_image
    im_gray = im_gray[0:720, 0:1280]                                                        #Resizing the image to required size i.e(1280,720) required image
    alpha=1.8                                                                               #Assigning alpha (contrast value)
    beta=30                                                                                 #Assigning beta  (brightness value)
    im_gray=cv2.addWeighted(im_gray,alpha,np.zeros(im_gray.shape,im_gray.dtype),0,beta)     #Adding contrast and brightness before initilizing the wiener filter
    
    im_colour = ip_image                                                                         #putting the ip_image in im_colour to have a 3 channeld im_colour (colour img)
    im_colour = im_colour[0:720, 0:1280]                                                         #Resizing the image to required size i.e(1280,720) required image
    im_colour=cv2.addWeighted(im_colour,alpha,np.zeros(im_colour.shape,im_colour.dtype),0,beta)  #Adding contrast and brightness before initilizing the wiener filter

    im_red = np.zeros_like(im_gray)                                                         #creating three arrays of same size as that of im_gray 
    im_green = np.zeros_like(im_gray)
    im_blue = np.zeros_like(im_gray)

    im_red = im_colour[..., 0]                                                              #Assigning the values in the above arrays from im_colour 
    im_green = im_colour[..., 1]                                                            #Assigning in the order red, green, blue from im_colour using [...,0],[...,1],[...,2]
    im_blue = im_colour[..., 2]

    im_colour = np.float32(im_colour)/255.0                                                 #Taking the array_images above and making it float and dividing it by 255 to get a* 
    im_gray = np.float32(im_gray)/255.0                                                     #*new array having all float values using (np.float32(array)/255) these values are eqiuvalent* 
    im_red = np.float32(im_red)/255.0                                                       #*to original bgr values but now are in float as we divided it by 255
    im_green = np.float32(im_green)/255.0                                                   #This is done to use them later in converting it to frequency domain
    im_blue = np.float32(im_blue)/255.0
                                                                                            
    im_red = Blurly_edge(im_red)
    im_green = Blurly_edge(im_green)                                                        #calling the blurly_edge function with (array as argument) and asssigning the returned* 
    im_blue = Blurly_edge(im_blue)                                                          #*values into back into the arrays so that the blur edges are rectified

    im_red = cv2.dft(im_red, flags=cv2.DFT_COMPLEX_OUTPUT)                                  #Converting the (arrays) into frequency domain along with complex numbers
    im_green = cv2.dft(im_green, flags=cv2.DFT_COMPLEX_OUTPUT)
    im_blue = cv2.dft(im_blue, flags=cv2.DFT_COMPLEX_OUTPUT)

    def wiener():
        angle = np.rad2deg(0.1370)                                                          #Assigning value to angle in rad of PSF
        PSF_Len = 21                                                                        #Assigning value to Length of PSF
        
        noise = 0.000310                                                                    #Using some minimal noise and then adding into image and removing it back later stage*
                                                                                            #*Doing this ensures that even if noise of such magnitude is present it will be removed
        psf = motion_kernel(angle, PSF_Len)                                                 #Calling motion_kernel
      
        psf /= psf.sum()                                            
        psf_pad = np.zeros_like(im_gray)                                                         #Creating a PSF pad to make it as same size as that of im_gray
        Kernel_Height, Kernel_Width = psf.shape
        psf_pad[:Kernel_Height, :Kernel_Width] = psf                                             #Defing the PSF_pad in terms of kernel (Height and width) to make the exact psf
        PSF_DFT1 = cv2.dft(psf_pad, flags=cv2.DFT_COMPLEX_OUTPUT, nonzeroRows = Kernel_Height)   #Converting PSF into frequency domain
        PSF_DFT2 = (PSF_DFT1**2).sum(-1)                                                         #Taking kind of mod of PSF_DFT2
        M_PSF = PSF_DFT1 / (PSF_DFT2 + noise)[...,np.newaxis]                                    #Finding a part of wiener filter to use it in actual formula of wiener filter

        SPEC_R = cv2.mulSpectrums(im_red, M_PSF, 0)                                              #Here the actual psf is multiplied with the blur img channel arrays*
        SPEC_G = cv2.mulSpectrums(im_green, M_PSF, 0)                                            #*and the blur is removed in the frequency domain it self
        SPEC_B = cv2.mulSpectrums(im_blue, M_PSF, 0)

        SPEC_R = cv2.idft(SPEC_R, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT )                    #Converting it back to space domain using idft and assigning it back to the channel array*
        SPEC_G = cv2.idft(SPEC_G, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT )                    #so we are now getting the space domain values in these array channels that are in float type
        SPEC_B = cv2.idft(SPEC_B, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT )

        SPEC_RGB = np.zeros_like(im_colour)                                                      
        SPEC_RGB[..., 0] = SPEC_R
        SPEC_RGB[..., 1] = SPEC_G
        SPEC_RGB[..., 2] = SPEC_B                                                                #Here we are creating back a 3 channeled array with deblured values

     
        SPEC_RGB = np.roll(SPEC_RGB, -Kernel_Height//2, 0)                                       #Here we are rolling the elements that are rolled beyond the last position are reintrodused at the first
        RGB_FIN = np.roll(SPEC_RGB, -Kernel_Width//2, 1)                                         #*at the first



        
        RGB_FLOAT = RGB_FIN.astype(np.float64)/SPEC_RGB.max()                                       #Here we are converting the float array into uint8 type by multiplying back*
        RGB_FLOAT_255 = 255 * RGB_FLOAT                                                             #*with 255 
        img_un8 = RGB_FLOAT_255.astype(np.uint8)
        
        kernel = np.ones((2,2),np.uint8)                                                            #To remove any small noises in the image using morphological opening*       
        mask_img = cv2.morphologyEx(img_un8,cv2.MORPH_OPEN,kernel, iterations =3)                   #*This noise arrises due to converting of float to uint8*

        alpha=1.7
        beta=0.9
        mask_imgnew=cv2.addWeighted(mask_img,alpha,np.zeros(mask_img.shape,mask_img.dtype),0,beta) #Adding little more contrast as it was lost during conversion of dtype of RGB_FLOAT
        
        imgfinal = cv2.medianBlur(mask_imgnew,3)                                                   #Applying median blur so as to reduce the ringing effect and edge noise (smoothing)
        
        return imgfinal
    
    ip_image = wiener()
    id_list = aruco_detection.detect(ip_image)                                                     #Calling the detect() function from aruco_detection from the codes folder
    
  
    return ip_image, id_list                                                                       #Returing the values to main function below


    
####################################################################
## The main program which provides read in input of one image at a
## time to process function in which you will code your generalized
## output computing code
## Do not modify this code!!!
####################################################################
def main(val):
    ################################################################
    ## variable declarations
    ################################################################
    i = 1
    ## reading in video 
    cap = cv2.VideoCapture(images_folder_path+"/"+"aruco_bot.mp4")
    ## getting the frames per second value of input video
    fps = cap.get(cv2.CAP_PROP_FPS)
    ## getting the frame sequence
    frame_seq = int(val)*fps
    ## setting the video counter to frame sequence
    cap.set(1,frame_seq)
    ## reading in the frame
    ret, frame = cap.read()
    ## verifying frame has content
    print(frame.shape)
    ## display to see if the frame is correct
    cv2.imshow("window", frame)
    cv2.waitKey(0);
    ## calling the algorithm function
    op_image, aruco_info = process(frame)
    ## saving the output in  a list variable
    line = [str(i), "Aruco_bot.jpg" , str(aruco_info[0]), str(aruco_info[3])]
    ## incrementing counter variable
    i+=1
    ## verifying all data
    print(line)
    ## writing to angles.csv in Generated folder without spaces
    with open(generated_folder_path+"/"+'output.csv', 'w') as writeFile:
        print("About to write csv")
        writer = csv.writer(writeFile)
        writer.writerow(line)
    ## closing csv file    
    writeFile.close()



    

############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main(input("time value in seconds:"))
