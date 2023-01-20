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
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar




cap = cv.VideoCapture(0)
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

    mask_inv = cv.bitwise_not(mask)
    
    mask_sm = cv.medianBlur(mask_inv, 13)

    # find contours 
    
    ret,thresh = cv.threshold(mask_sm,127,255,0)
    contours, _ = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    
    
    cv.drawContours(frame, contours, -1, 255, 3)

    
    for i in contours:
        if (cv.contourArea(i)>650 and cv.contourArea(i)<10000):
            x,y,w,h = cv.boundingRect(i)
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv.rectangle(mask_sm,(x,y),(x+w,y+h),(0,0,255),2)
            
            
            #color detection
            img = frame[y:y+h, x:x+w]
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
            clt = KMeans(n_clusters=3) #cluster number
            clt.fit(img)

            hist = find_histogram(clt)
            bar = plot_colors2(hist, clt.cluster_centers_)

            cv.imshow('bar', bar)
            
    
    '''
    #draw all contours 
    for i in range(0, len(contours), 1):
        x,y,w,h = cv.boundingRect(contours[i])
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        cv.rectangle(mask_sm,(x,y),(x+w,y+h),(0,0,255),2)
    '''
    
    cv.imshow('frame',frame)
    cv.imshow('mask',mask_sm)
    cv.imshow('res',res)
    
    

    
    
    #produce boxed frame and cropped boxed frame 
    #boxed,cropped = draw_bounding_box(contours, img)
    
    
    
    
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()