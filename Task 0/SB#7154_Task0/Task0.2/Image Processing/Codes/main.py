import cv2
import numpy as np
import os
import csv

#The following function finds the properties of the images viz. (1)Name of the image w/ extension (ii)Dimensions of the image (iii) Value of the colour triplet B.G,R at (M/2,N/2)
def partA():
    
    imgpath1="..\\Images\\bird.jpg"
    img1 =cv2.imread(imgpath1)
    x1=int(img1.shape[0])/2
    y1=int(img1.shape[1])/2
    a1=img1[int(x1),int(y1)]        
        
    imgpath2="..\\Images\\cat.jpg"
    img2 =cv2.imread(imgpath2)
    x2=int(img2.shape[0])/2
    y2=int(img2.shape[1])/2
    a2=img2[int(x2),int(y2)]       
    
    imgpath3="..\\Images\\flowers.jpg"
    img3 =cv2.imread(imgpath3)
    x3=int(img3.shape[0])/2
    y3=int(img3.shape[1])/2
    a3=img3[int(x3),int(y3)]

    imgpath4="..\\Images\\horse.jpg"
    img4 =cv2.imread(imgpath4)
    x4=int(img4.shape[0])/2
    y4=int(img4.shape[1])/2
    a4=img4[int(x4),int(y4)]
    with open('..\\Generated\\stats.csv','w',newline='') as f:
        thewriter=csv.writer(f)
        thewriter.writerow([os.path.basename(imgpath1),img1.shape[0],img1.shape[1],img1.shape[2],a1[0],a1[1],a1[2]])
        thewriter.writerow([os.path.basename(imgpath2),img2.shape[0],img2.shape[1],img2.shape[2],a2[0],a2[1],a2[2]])
        thewriter.writerow([os.path.basename(imgpath3),img3.shape[0],img3.shape[1],img3.shape[2],a3[0],a3[1],a3[2]])
        thewriter.writerow([os.path.basename(imgpath4),img4.shape[0],img4.shape[1],img4.shape[2],a4[0],a4[1],a4[2]])


#The following function reads the image "cat.jpg" and set the blue and green channels to zero and visualizes the red component 
def partB():
    imgpathB="..\\Images\\cat.jpg"
    imgB =cv2.imread(imgpathB)
    B,G,R=cv2.split(imgB)
    zeros=np.zeros(imgB.shape,dtype="uint8")
    newimgB=cv2.merge([zeros,zeros,R])
    cv2.imwrite('..\\Generated\\cat_red.jpg',newimgB)

#The following function reads the image "flower.jpg" which is three channeled and sets the value of the fourth channel i.e alpha to 255/2 and increases the overall transparency by 50%
def partC():
    imgpathC="..\\Images\\flowers.jpg"
    imgC =cv2.imread(imgpathC)
    B,G,R=cv2.split(imgC)
    alpha = np.zeros([imgC.shape[0],imgC.shape[1],1], dtype=np.uint8) + 127.5
    newimgC = np.dstack((imgC,alpha))
    cv2.imwrite('..\\Generated\\flowers_alpha.png',newimgC)
   
#The following function reads the image "horse.jpg" and the intensity level component of every pixel is computed and the image is saved as one channeled(greyscale) 
def partD():
    imgpathD= "..\\Images\\horse.jpg"
    imgD = cv2.imread(imgpathD,1)
    B, G, R = cv2.split(imgD)
    I = ((0.3 * R)+(0.59 * G)+(0.11 * B))
    cv2.imwrite('..\\Generated\\horse_gray.jpg',I)
    
#Calling the above functions
partA()
partB()
partC()
partD()
