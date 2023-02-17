#code sources:
#https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
#https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html

#improvements:
# invert mask for contouring 
# add in contour tracking
# blur mask to elimminate noise from camera 
# add in threshold for contour area to select correct contour of the desired object 
import cv2 as cv
import numpy as np


cap = cv.VideoCapture(0)

# for recoding purposes
'''
width= int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

writer= cv.VideoWriter('detection.mp4', cv.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
'''

while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([80,50,50])
    upper_blue = np.array([130,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)
    
    # use median filter to filter out the camera noise 
    mask_sm = cv.medianBlur(mask, 13)

    # find contours 
    contours, hierachy = cv.findContours(mask_sm,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
 
    # draw all contours(for analysis)
    cv.drawContours(frame, contours, -1, 255, 3)
    
    #find largest contour area
    contour_size = np.ones(len(contours))
    for i in range(len(contours)):
        contour_size[i] = cv.contourArea(contours[i])
    
    # graph the largest contour 
    for i in contours:
        if cv.contourArea(i) == max(contour_size):
            x,y,w,h = cv.boundingRect(i)
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv.rectangle(mask_sm,(x,y),(x+w,y+h),(0,0,255),2)
            
    # put the frame in the window 
    cv.imshow('frame',frame)
    cv.imshow('mask',mask_sm)
    cv.imshow('res',res)
    
    #writer.write(frame)
    

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
writer.release()
cv.destroyAllWindows()