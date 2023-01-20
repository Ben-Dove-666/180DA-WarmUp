import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

cap = cv2.VideoCapture(0)
################################################### functions ##################################################
# below are from:
# https://www.freedomvc.com/index.php/2021/06/26/contours-and-bounding-boxes/

# contour functions for drawing contour on complex shapes 
# This function allows us to create a descending sorted list of contour areas.
def contour_area(contours):
     
    # create an empty list
    cnt_area = []
     
    # loop through all the contours
    for i in range(0,len(contours),1):
        # for each contour, use OpenCV to calculate the area of the contour
        cnt_area.append(cv2.contourArea(contours[i]))
 
    # Sort our list of contour areas in descending order
    list.sort(cnt_area, reverse=True)
    return cnt_area

def draw_bounding_box(contours, image, number_of_boxes=0):
    # Call our function to get the list of contour areas
    cnt_area = contour_area(contours)
 
    # Loop through each contour of our image
    for i in range(0,len(contours),1):
        cnt = contours[i]
 
        # Only draw the the largest number of boxes
        if (cv2.contourArea(cnt) == cnt_area[number_of_boxes]):
             
            # Use OpenCV boundingRect function to get the details of the contour
            x,y,w,h = cv2.boundingRect(cnt)
             
            # crop by typing y first then x 
            # also do this before next step so the rect line is not in cropped image
            cropped = image[y:y+h, x:x+w]
            # Draw the bounding box
            image=cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
         
    return image, cropped 

# below is written by me 
# compile all boxing into one function
# para: img: the frame, lower/upper_col: threshold values for item detection based on color, default to blue 
def box(img, lower_col=np.array([110,50,50]), upper_col=np.array([130,255,255])):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image to get only specified colors
    mask = cv2.inRange(hsv, lower_col, upper_col)
    # Bitwise-AND mask and original image
    # res = cv.bitwise_and(frame,frame, mask= mask)
    
    # use mask for box 
    # invert mask so the box is right 
    mask_inv = cv2.bitwise_not(mask)

    # find contours 
    ret,thresh = cv2.threshold(mask_inv,127,255,0)
    contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #produce boxed frame and cropped boxed frame 
    boxed,cropped = draw_bounding_box(contours, img)
    
    return boxed, cropped


while(1):
    # Take each frame
    _, frame = cap.read()
    
    a,b = box(frame)
    cv2.imshow('boxed',a)    
    cv2.imshow('cropped',b)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()